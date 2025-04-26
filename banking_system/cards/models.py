import random
import string
from datetime import datetime, timedelta
from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password
from django.core.validators import MinValueValidator
from decimal import Decimal

User = get_user_model()


def generate_card_number():
    """Generate a random 16-digit card number"""
    return ''.join(random.choices(string.digits, k=16))


def generate_cvv():
    """Generate a random 3-digit CVV"""
    return ''.join(random.choices(string.digits, k=3))


def default_expiry_date():
    """Default expiry date is 3 years from now"""
    return datetime.now() + timedelta(days=3*365)


class Card(models.Model):
    """
    Model for virtual debit/credit cards
    """
    CARD_TYPES = (
        ('debit', 'Debit Card'),
        ('credit', 'Credit Card'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cards')
    card_number = models.CharField(max_length=16, unique=True)
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    expiry_date = models.DateField(default=default_expiry_date)
    cvv = models.CharField(max_length=128)  # Hashed CVV for security
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Card'
        verbose_name_plural = 'Cards'
    
    def __str__(self):
        return f"{self.get_card_type_display()} - {self.masked_card_number}"
    
    def save(self, *args, **kwargs):
        # Generate card details if new card
        if not self.pk:
            # Generate card number if not provided
            if not self.card_number:
                self.card_number = generate_card_number()
            
            # Generate and hash CVV
            raw_cvv = generate_cvv()
            self.set_cvv(raw_cvv)
            
            # Store raw values temporarily for first-time display
            self._raw_cvv = raw_cvv
        
        super().save(*args, **kwargs)
    
    def set_cvv(self, cvv):
        """Hash and store CVV"""
        self.cvv = make_password(cvv)
    
    def check_cvv(self, cvv):
        """Verify CVV"""
        return check_password(cvv, self.cvv)
    
    @property
    def masked_card_number(self):
        """Return masked card number for display"""
        if self.card_number:
            return f"{'*' * 12}{self.card_number[-4:]}"
        return ""
    
    @property
    def is_expired(self):
        """Check if card is expired"""
        return datetime.now().date() > self.expiry_date
    
    def deactivate(self):
        """Deactivate the card"""
        self.is_active = False
        self.save()
    
    def fund(self, amount):
        """Add funds to card from linked account"""
        if amount <= 0:
            raise ValueError("Fund amount must be positive")
        
        self.balance += amount
        self.save()
        return self.balance
    
    def withdraw_to_account(self, amount):
        """Move funds from card to linked account"""
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        
        if amount > self.balance:
            raise ValueError("Insufficient card balance")
        
        self.balance -= amount
        self.save()
        return self.balance
