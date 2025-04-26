from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction as db_transaction
from django.shortcuts import render, redirect
from accounts.models import Account
from .forms import FundTransferForm
from .models import Transaction


@login_required
def transfer_money(request):
    """
    View for transferring money to another account
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to make transfers.')
        return redirect('users:verify_email')
    
    user_account = request.user.account
    
    # Check if account is active
    if not user_account.is_active:
        messages.error(request, 'Your account is currently frozen. Please contact support.')
        return redirect('dashboard:user_dashboard')
    
    if request.method == 'POST':
        form = FundTransferForm(request.POST, user_account=user_account)
        if form.is_valid():
            recipient_account_number = form.cleaned_data['recipient_account']
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            
            # Get recipient account
            recipient_account = Account.objects.get(account_number=recipient_account_number)
            
            try:
                # Perform transfer within a transaction block
                with db_transaction.atomic():
                    # Lock both accounts for update
                    sender_account = Account.objects.select_for_update().get(id=user_account.id)
                    recipient = Account.objects.select_for_update().get(id=recipient_account.id)
                    
                    # Perform withdrawal and deposit
                    sender_account.withdraw(amount)
                    recipient.deposit(amount)
                    
                    # Create transaction record
                    Transaction.create_transfer(
                        sender_account,
                        recipient,
                        amount,
                        description
                    )
                
                messages.success(
                    request, 
                    f'Successfully transferred {amount} to account {recipient_account_number}'
                )
                return redirect('transactions:transaction_history')
                
            except ValueError as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, f'Transfer failed: {str(e)}')
    else:
        form = FundTransferForm(user_account=user_account)
    
    return render(request, 'transactions/transfer_money.html', {'form': form})


@login_required
def transaction_history(request):
    """
    View for displaying transaction history
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to view transaction history.')
        return redirect('users:verify_email')
    
    user_account = request.user.account
    
    # Get all transactions where user is sender or recipient
    transactions = Transaction.objects.filter(
        account=user_account
    ) | Transaction.objects.filter(
        recipient_account=user_account
    )
    transactions = transactions.order_by('-timestamp')
    
    return render(request, 'transactions/transaction_history.html', {'transactions': transactions})
