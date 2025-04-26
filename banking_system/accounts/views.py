from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ChangePinForm
from transactions.models import Transaction


@login_required
def account_detail(request):
    """
    View for account details and transaction history
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to access your account details.')
        return redirect('users:verify_email')
    
    account = request.user.account
    recent_transactions = Transaction.objects.filter(
        account=account
    ).order_by('-timestamp')[:10]
    
    context = {
        'account': account,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'accounts/account_detail.html', context)


@login_required
def change_pin(request):
    """
    View for changing account PIN
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to change your PIN.')
        return redirect('users:verify_email')
    
    account = request.user.account
    
    if request.method == 'POST':
        form = ChangePinForm(request.POST, account=account)
        if form.is_valid():
            new_pin = form.cleaned_data['new_pin']
            account.set_pin(new_pin)
            account.save()
            messages.success(request, 'Your PIN has been successfully changed.')
            return redirect('accounts:account_detail')
    else:
        form = ChangePinForm()
    
    return render(request, 'accounts/change_pin.html', {'form': form})
