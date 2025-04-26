from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from accounts.models import Account
from .models import Card

User = get_user_model()


class CardModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            full_name='Test User',
            password='testpassword123'
        )
        self.account = Account.objects.get(user=self.user)
        self.account.balance = Decimal('1000.00')
        self.account.save()
    
    def test_card_creation(self):
        """Test creating a new card"""
        card = Card.objects.create(
            user=self.user,
            card_type='debit'
        )
        
        # Check card details
        self.assertEqual(len(card.card_number), 16)
        self.assertTrue(card.card_number.isdigit())
        self.assertEqual(card.card_type, 'debit')
        self.assertEqual(card.balance, Decimal('0.00'))
        self.assertTrue(card.is_active)
        self.assertIsNotNone(card.cvv)
        
        # Check expiry date is in the future
        self.assertTrue(card.expiry_date > timezone.now().date())
    
    def test_card_funding(self):
        """Test funding a card"""
        card = Card.objects.create(
            user=self.user,
            card_type='debit'
        )
        
        initial_card_balance = card.balance
        fund_amount = Decimal('200.00')
        
        # Fund the card
        new_balance = card.fund(fund_amount)
        self.assertEqual(new_balance, initial_card_balance + fund_amount)
        
        # Check persistence
        card.refresh_from_db()
        self.assertEqual(card.balance, initial_card_balance + fund_amount)
        
        # Test invalid funding
        with self.assertRaises(ValueError):
            card.fund(Decimal('-50.00'))
    
    def test_withdraw_to_account(self):
        """Test withdrawing from card to account"""
        card = Card.objects.create(
            user=self.user,
            card_type='debit',
            balance=Decimal('500.00')
        )
        
        initial_card_balance = card.balance
        withdraw_amount = Decimal('200.00')
        
        # Withdraw from card
        new_balance = card.withdraw_to_account(withdraw_amount)
        self.assertEqual(new_balance, initial_card_balance - withdraw_amount)
        
        # Check persistence
        card.refresh_from_db()
        self.assertEqual(card.balance, initial_card_balance - withdraw_amount)
        
        # Test invalid withdrawal
        with self.assertRaises(ValueError):
            card.withdraw_to_account(Decimal('-50.00'))
        
        # Test insufficient balance
        with self.assertRaises(ValueError):
            card.withdraw_to_account(card.balance + Decimal('100.00'))
    
    def test_card_expiry_check(self):
        """Test card expiry check"""
        # Create card with expiry date in the past
        expired_card = Card.objects.create(
            user=self.user,
            card_type='debit',
            expiry_date=timezone.now().date() - timedelta(days=1)
        )
        self.assertTrue(expired_card.is_expired)
        
        # Create card with future expiry date
        valid_card = Card.objects.create(
            user=self.user,
            card_type='credit',
            expiry_date=timezone.now().date() + timedelta(days=365)
        )
        self.assertFalse(valid_card.is_expired)
    
    def test_card_deactivation(self):
        """Test card deactivation"""
        card = Card.objects.create(
            user=self.user,
            card_type='debit'
        )
        self.assertTrue(card.is_active)
        
        card.deactivate()
        self.assertFalse(card.is_active)
