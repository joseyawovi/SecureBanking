from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Account


class PinVerificationForm(forms.Form):
    """
    Form for verifying account PIN
    """
    pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your 4-digit PIN'}),
        min_length=4,
        max_length=4
    )
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        super().__init__(*args, **kwargs)
    
    def clean_pin(self):
        pin = self.cleaned_data.get('pin')
        if not pin.isdigit():
            raise ValidationError("PIN must contain only digits.")
        
        # Check if PIN is correct (account is passed from the view)
        if self.account and not self.account.check_pin(pin):
            raise ValidationError("Incorrect PIN.")
        
        return pin


class ChangePinForm(forms.Form):
    """
    Form for changing account PIN
    """
    current_pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter current PIN'}),
        min_length=4,
        max_length=4
    )
    new_pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter new PIN'}),
        min_length=4,
        max_length=4
    )
    confirm_pin = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm new PIN'}),
        min_length=4,
        max_length=4
    )
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        super().__init__(*args, **kwargs)
    
    def clean_current_pin(self):
        current_pin = self.cleaned_data.get('current_pin')
        if not current_pin.isdigit():
            raise ValidationError("PIN must contain only digits.")
        
        # Verify current PIN
        if self.account and not self.account.check_pin(current_pin):
            raise ValidationError("Current PIN is incorrect.")
        
        return current_pin
    
    def clean_new_pin(self):
        new_pin = self.cleaned_data.get('new_pin')
        if not new_pin.isdigit():
            raise ValidationError("PIN must contain only digits.")
        
        # Check for sequential or repeated digits
        if re.match(r'(\d)\1{3}', new_pin):  # Check for repeated digits like 1111
            raise ValidationError("PIN cannot have the same digit repeated.")
        
        if new_pin in ('1234', '2345', '3456', '4567', '5678', '6789', '9876', '8765', '7654', '6543', '5432', '4321'):
            raise ValidationError("PIN cannot be a simple sequence.")
        
        return new_pin
    
    def clean(self):
        cleaned_data = super().clean()
        new_pin = cleaned_data.get('new_pin')
        confirm_pin = cleaned_data.get('confirm_pin')
        
        if new_pin and confirm_pin and new_pin != confirm_pin:
            self.add_error('confirm_pin', "New PIN and confirmation do not match.")
        
        return cleaned_data
