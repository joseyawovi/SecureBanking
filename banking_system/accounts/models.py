import random
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password

User = get_user_model()


class Account(models.Model):
    """
    Bank account model with account details
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account')
    account_number = models.CharField(max_length=12, unique=True, editable=False)
    balance = models.DecimalField(
        max_digits=12, 
        decimal_places=2, 
        default=0.00, 
        validators=[MinValueValidator(0.00)]
    )
    pin_hash = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Account {self.account_number} - {self.user.full_name}"
    
    def save(self, *args, **kwargs):
        # Generate a unique account number if not already set
        if not self.account_number:
            self.account_number = self._generate_account_number()
        
        # If PIN is updated directly (not through set_pin method)
        if not self.pin_hash:
            default_pin = ''.join(random.choices('0123456789', k=4))
            self.set_pin(default_pin)
            
        super().save(*args, **kwargs)
    
    def _generate_account_number(self):
        """Generate a unique 12-digit account number"""
        while True:
            number = ''.join(random.choices('0123456789', k=12))
            if not Account.objects.filter(account_number=number).exists():
                return number
    
    def set_pin(self, pin):
        """Set a new PIN (hashed for security)"""
        self.pin_hash = make_password(pin)
    
    def check_pin(self, pin):
        """Verify PIN"""
        return check_password(pin, self.pin_hash)
    
    def deposit(self, amount):
        """Add funds to account"""
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        
        self.balance += amount
        self.save(update_fields=['balance', 'updated_at'])
        return self.balance
    
    def withdraw(self, amount):
        """Remove funds from account if sufficient balance exists"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        
        self.balance -= amount
        self.save(update_fields=['balance', 'updated_at'])
        return self.balance
    
    def freeze(self):
        """Freeze the account"""
        self.is_active = False
        self.save(update_fields=['is_active', 'updated_at'])
    
    def unfreeze(self):
        """Unfreeze/activate the account"""
        self.is_active = True
        self.save(update_fields=['is_active', 'updated_at'])
