import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Account

User = get_user_model()


@receiver(post_save, sender=User)
def create_account(sender, instance, created, **kwargs):
    """
    Create a bank account when a new user is registered
    """
    if created:
        # Generate a random 4-digit PIN for the account
        pin = ''.join(random.choices('0123456789', k=4))
        
        # Create a new account with initial balance of 1000.00
        account = Account(user=instance)
        account.set_pin(pin)
        account.balance = 1000.00  # Initial balance for testing
        account.save()
