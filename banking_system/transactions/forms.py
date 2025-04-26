from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Transaction


class FundTransferForm(forms.Form):
    """
    Form for transferring funds to another account
    """
    recipient_account = forms.CharField(
        max_length=12,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter recipient account number'})
    )
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
    )
    description = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter description (optional)'})
    )
    pin = forms.CharField(
        max_length=4,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your PIN'})
    )
    
    def __init__(self, *args, **kwargs):
        self.user_account = kwargs.pop('user_account', None)
        super().__init__(*args, **kwargs)
    
    def clean_recipient_account(self):
        from accounts.models import Account
        
        recipient_account_number = self.cleaned_data.get('recipient_account')
        
        # Check if recipient account exists
        try:
            recipient_account = Account.objects.get(account_number=recipient_account_number)
        except Account.DoesNotExist:
            raise ValidationError("Recipient account not found.")
        
        # Check if recipient account is active
        if not recipient_account.is_active:
            raise ValidationError("The recipient account is inactive.")
        
        # Check if user is trying to transfer to own account
        if self.user_account and recipient_account.account_number == self.user_account.account_number:
            raise ValidationError("You cannot transfer funds to your own account.")
        
        return recipient_account_number
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        # Ensure amount is positive
        if amount <= 0:
            raise ValidationError("Transfer amount must be greater than zero.")
        
        # Check if user has sufficient balance
        if self.user_account and amount > self.user_account.balance:
            raise ValidationError("Insufficient balance for this transfer.")
        
        return amount
    
    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        
        # Validate PIN format
        if not pin.isdigit() or len(pin) != 4:
            raise ValidationError("PIN must be a 4-digit number.")
        
        # Verify PIN against account
        if self.user_account and not self.user_account.check_pin(pin):
            raise ValidationError("Incorrect PIN.")
        
        return pin
