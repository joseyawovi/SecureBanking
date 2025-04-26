from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Card
from .forms import CreateCardForm, FundCardForm, WithdrawFromCardForm
from transactions.models import Transaction


@login_required
def card_list(request):
    """
    View to list all user's cards
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to access cards.')
        return redirect('users:verify_email')
    
    cards = Card.objects.filter(user=request.user)
    
    return render(request, 'cards/card_list.html', {'cards': cards})


@login_required
def create_card(request):
    """
    View to create a new virtual card
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to create cards.')
        return redirect('users:verify_email')
    
    if request.method == 'POST':
        form = CreateCardForm(request.POST, user=request.user)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            
            # Store card details for one-time display
            request.session['new_card'] = {
                'id': card.id,
                'card_number': card.card_number,
                'cvv': card._raw_cvv,
                'expiry_date': card.expiry_date.strftime('%m/%y')
            }
            
            messages.success(request, 'Card created successfully! Please note your card details shown below.')
            return redirect('cards:card_detail', card_id=card.id)
    else:
        form = CreateCardForm(user=request.user)
    
    return render(request, 'cards/create_card.html', {'form': form})


@login_required
def card_detail(request, card_id):
    """
    View to show card details
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to view card details.')
        return redirect('users:verify_email')
    
    card = get_object_or_404(Card, id=card_id, user=request.user)
    
    # Get the new card details from session if available (one-time display)
    new_card_details = None
    if 'new_card' in request.session and request.session['new_card']['id'] == card.id:
        new_card_details = request.session['new_card']
        del request.session['new_card']
    
    context = {
        'card': card,
        'new_card_details': new_card_details
    }
    
    return render(request, 'cards/card_detail.html', context)


@login_required
def fund_card(request, card_id):
    """
    View to fund a card from account balance
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to fund cards.')
        return redirect('users:verify_email')
    
    card = get_object_or_404(Card, id=card_id, user=request.user)
    
    # Check if card is active
    if not card.is_active:
        messages.error(request, 'This card is inactive and cannot be funded.')
        return redirect('cards:card_detail', card_id=card.id)
    
    # Check if card is expired
    if card.is_expired:
        messages.error(request, 'This card is expired and cannot be funded.')
        return redirect('cards:card_detail', card_id=card.id)
    
    if request.method == 'POST':
        form = FundCardForm(request.POST, user=request.user, card=card)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            try:
                # Perform funding within a transaction block
                with db_transaction.atomic():
                    # Get account with lock
                    account = request.user.account
                    
                    # Withdraw from account
                    account.withdraw(amount)
                    
                    # Add to card
                    card.fund(amount)
                    
                    # Create transaction record
                    Transaction.create_card_funding(
                        account,
                        amount,
                        f'Funding card ending in {card.card_number[-4:]}'
                    )
                
                messages.success(request, f'Successfully funded card with {amount}.')
                return redirect('cards:card_detail', card_id=card.id)
                
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Funding failed: {str(e)}')
    else:
        form = FundCardForm(user=request.user, card=card)
    
    return render(request, 'cards/fund_card.html', {'form': form, 'card': card})


@login_required
def withdraw_from_card(request, card_id):
    """
    View to withdraw from card to account
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to withdraw from cards.')
        return redirect('users:verify_email')
    
    card = get_object_or_404(Card, id=card_id, user=request.user)
    
    # Check if card is active
    if not card.is_active:
        messages.error(request, 'This card is inactive and cannot be withdrawn from.')
        return redirect('cards:card_detail', card_id=card.id)
    
    if request.method == 'POST':
        form = WithdrawFromCardForm(request.POST, user=request.user, card=card)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            
            try:
                # Perform withdrawal within a transaction block
                with db_transaction.atomic():
                    # Get account with lock
                    account = request.user.account
                    
                    # Withdraw from card
                    card.withdraw_to_account(amount)
                    
                    # Deposit to account
                    account.deposit(amount)
                    
                    # Create transaction record
                    Transaction.create_deposit(
                        account,
                        amount,
                        f'Withdrawal from card ending in {card.card_number[-4:]}'
                    )
                
                messages.success(request, f'Successfully withdrawn {amount} from card to account.')
                return redirect('cards:card_detail', card_id=card.id)
                
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Withdrawal failed: {str(e)}')
    else:
        form = WithdrawFromCardForm(user=request.user, card=card)
    
    return render(request, 'cards/withdraw_from_card.html', {'form': form, 'card': card})


@login_required
def deactivate_card(request, card_id):
    """
    View to deactivate a card
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to manage cards.')
        return redirect('users:verify_email')
    
    card = get_object_or_404(Card, id=card_id, user=request.user)
    
    if request.method == 'POST':
        card.deactivate()
        messages.success(request, 'Card has been deactivated successfully.')
        return redirect('cards:card_list')
    
    return render(request, 'cards/deactivate_card.html', {'card': card})
