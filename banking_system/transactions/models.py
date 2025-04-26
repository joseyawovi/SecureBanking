import uuid
from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from accounts.models import Account


class Transaction(models.Model):
    """
    Model for fund transfer transactions
    """
    TRANSACTION_TYPES = (
        ('transfer', 'Transfer'),
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('card_funding', 'Card Funding'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    
    reference_id = models.CharField(max_length=36, unique=True, editable=False)
    transaction_type = models.CharField(max_length=15, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.CharField(max_length=100, blank=True)
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    recipient_account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name='received_transactions',
        null=True,
        blank=True
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    failure_reason = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
    
    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.reference_id}"
    
    def save(self, *args, **kwargs):
        # Generate a unique reference ID if not already set
        if not self.reference_id:
            self.reference_id = str(uuid.uuid4())
        
        super().save(*args, **kwargs)
    
    @classmethod
    def create_transfer(cls, from_account, to_account, amount, description=''):
        """
        Create a transfer transaction
        """
        return cls.objects.create(
            transaction_type='transfer',
            amount=amount,
            description=description,
            account=from_account,
            recipient_account=to_account,
            status='completed'
        )
    
    @classmethod
    def create_deposit(cls, to_account, amount, description=''):
        """
        Create a deposit transaction
        """
        return cls.objects.create(
            transaction_type='deposit',
            amount=amount,
            description=description,
            account=to_account,
            status='completed'
        )
    
    @classmethod
    def create_withdrawal(cls, from_account, amount, description=''):
        """
        Create a withdrawal transaction
        """
        return cls.objects.create(
            transaction_type='withdrawal',
            amount=amount,
            description=description,
            account=from_account,
            status='completed'
        )
    
    @classmethod
    def create_card_funding(cls, from_account, amount, description=''):
        """
        Create a card funding transaction
        """
        return cls.objects.create(
            transaction_type='card_funding',
            amount=amount,
            description=description,
            account=from_account,
            status='completed'
        )
