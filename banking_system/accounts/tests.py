from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Account

User = get_user_model()


class AccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            full_name='Test User',
            password='testpassword123'
        )
        self.account = Account.objects.get(user=self.user)  # Account created by signal
    
    def test_account_creation(self):
        """Test that account is created automatically for new user"""
        self.assertIsNotNone(self.account)
        self.assertEqual(len(self.account.account_number), 12)
        self.assertEqual(self.account.balance, Decimal('1000.00'))
        self.assertTrue(self.account.is_active)
    
    def test_pin_hash_functionality(self):
        """Test PIN hashing and verification"""
        test_pin = '1234'
        self.account.set_pin(test_pin)
        self.assertTrue(self.account.check_pin(test_pin))
        self.assertFalse(self.account.check_pin('4321'))
    
    def test_deposit_functionality(self):
        """Test deposit functionality"""
        initial_balance = self.account.balance
        deposit_amount = Decimal('500.00')
        
        new_balance = self.account.deposit(deposit_amount)
        self.assertEqual(new_balance, initial_balance + deposit_amount)
        
        # Refresh from DB to check persistence
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, initial_balance + deposit_amount)
        
        # Test negative deposit
        with self.assertRaises(ValueError):
            self.account.deposit(Decimal('-100.00'))
    
    def test_withdraw_functionality(self):
        """Test withdraw functionality"""
        initial_balance = self.account.balance
        withdraw_amount = Decimal('300.00')
        
        new_balance = self.account.withdraw(withdraw_amount)
        self.assertEqual(new_balance, initial_balance - withdraw_amount)
        
        # Refresh from DB to check persistence
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, initial_balance - withdraw_amount)
        
        # Test withdraw more than balance
        with self.assertRaises(ValueError):
            self.account.withdraw(self.account.balance + Decimal('100.00'))
        
        # Test negative withdraw
        with self.assertRaises(ValueError):
            self.account.withdraw(Decimal('-100.00'))
    
    def test_freeze_unfreeze(self):
        """Test account freezing and unfreezing"""
        self.assertTrue(self.account.is_active)
        
        self.account.freeze()
        self.assertFalse(self.account.is_active)
        
        self.account.unfreeze()
        self.assertTrue(self.account.is_active)
