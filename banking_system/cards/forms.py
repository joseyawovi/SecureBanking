from django import forms
from django.core.exceptions import ValidationError
from decimal import Decimal
from .models import Card
from accounts.models import Account


class CreateCardForm(forms.ModelForm):
    """
    Form for creating a new virtual card
    """
    pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter account PIN'}),
        min_length=4,
        max_length=4,
        help_text='Enter your account PIN to authorize card creation'
    )
    
    class Meta:
        model = Card
        fields = ['card_type']
        widgets = {
            'card_type': forms.Select(attrs={'class': 'form-control'})
        }
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        
        # Validate PIN
        if not pin.isdigit():
            raise ValidationError("PIN must contain only digits.")
        
        # Verify PIN against account
        if self.user and not self.user.account.check_pin(pin):
            raise ValidationError("Incorrect PIN.")
        
        return pin


class FundCardForm(forms.Form):
    """
    Form for funding a card from account balance
    """
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
    )
    pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter account PIN'}),
        min_length=4,
        max_length=4
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.card = kwargs.pop('card', None)
        super().__init__(*args, **kwargs)
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        # Check if amount is valid
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        
        # Check if user has sufficient balance
        if self.user and amount > self.user.account.balance:
            raise ValidationError("Insufficient account balance.")
        
        return amount
    
    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        
        # Validate PIN
        if not pin.isdigit():
            raise ValidationError("PIN must contain only digits.")
        
        # Verify PIN against account
        if self.user and not self.user.account.check_pin(pin):
            raise ValidationError("Incorrect PIN.")
        
        return pin


class WithdrawFromCardForm(forms.Form):
    """
    Form for withdrawing money from card to account
    """
    amount = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter amount'})
    )
    pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter account PIN'}),
        min_length=4,
        max_length=4
    )
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.card = kwargs.pop('card', None)
        super().__init__(*args, **kwargs)
    
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        
        # Check if amount is valid
        if amount <= 0:
            raise ValidationError("Amount must be greater than zero.")
        
        # Check if card has sufficient balance
        if self.card and amount > self.card.balance:
            raise ValidationError("Insufficient card balance.")
        
        return amount
    
    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        
        # Validate PIN
        if not pin.isdigit():
            raise ValidationError("PIN must contain only digits.")
        
        # Verify PIN against account
        if self.user and not self.user.account.check_pin(pin):
            raise ValidationError("Incorrect PIN.")
        
        return pin
