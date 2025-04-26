from decimal import Decimal
from django.test import TestCase
from django.db import transaction as db_transaction
from django.contrib.auth import get_user_model
from accounts.models import Account
from .models import Transaction

User = get_user_model()


class TransactionModelTest(TestCase):
    def setUp(self):
        # Create two users with accounts
        self.user1 = User.objects.create_user(
            email='user1@example.com',
            full_name='User One',
            password='password123'
        )
        self.account1 = Account.objects.get(user=self.user1)
        self.account1.balance = Decimal('1000.00')
        self.account1.save()
        
        self.user2 = User.objects.create_user(
            email='user2@example.com',
            full_name='User Two',
            password='password123'
        )
        self.account2 = Account.objects.get(user=self.user2)
    
    def test_transaction_creation(self):
        """Test creating different types of transactions"""
        # Test transfer transaction
        transfer_tx = Transaction.create_transfer(
            self.account1, 
            self.account2, 
            Decimal('100.00'), 
            'Test transfer'
        )
        self.assertEqual(transfer_tx.transaction_type, 'transfer')
        self.assertEqual(transfer_tx.amount, Decimal('100.00'))
        self.assertEqual(transfer_tx.status, 'completed')
        
        # Test deposit transaction
        deposit_tx = Transaction.create_deposit(
            self.account1, 
            Decimal('200.00'), 
            'Test deposit'
        )
        self.assertEqual(deposit_tx.transaction_type, 'deposit')
        self.assertEqual(deposit_tx.amount, Decimal('200.00'))
        self.assertEqual(deposit_tx.status, 'completed')
        
        # Test withdrawal transaction
        withdrawal_tx = Transaction.create_withdrawal(
            self.account1, 
            Decimal('50.00'), 
            'Test withdrawal'
        )
        self.assertEqual(withdrawal_tx.transaction_type, 'withdrawal')
        self.assertEqual(withdrawal_tx.amount, Decimal('50.00'))
        self.assertEqual(withdrawal_tx.status, 'completed')
    
    def test_atomic_transfer(self):
        """Test atomic transfer between accounts"""
        initial_balance1 = self.account1.balance
        initial_balance2 = self.account2.balance
        
        transfer_amount = Decimal('500.00')
        
        # Perform atomic transfer
        with db_transaction.atomic():
            self.account1 = Account.objects.select_for_update().get(id=self.account1.id)
            self.account2 = Account.objects.select_for_update().get(id=self.account2.id)
            
            # Withdraw from account1
            self.account1.withdraw(transfer_amount)
            
            # Deposit to account2
            self.account2.deposit(transfer_amount)
            
            # Create transaction record
            Transaction.create_transfer(
                self.account1, 
                self.account2, 
                transfer_amount, 
                'Test atomic transfer'
            )
        
        # Refresh from DB
        self.account1.refresh_from_db()
        self.account2.refresh_from_db()
        
        # Check balances
        self.assertEqual(self.account1.balance, initial_balance1 - transfer_amount)
        self.assertEqual(self.account2.balance, initial_balance2 + transfer_amount)
        
        # Check transaction record
        tx = Transaction.objects.get(transaction_type='transfer', amount=transfer_amount)
        self.assertEqual(tx.account, self.account1)
        self.assertEqual(tx.recipient_account, self.account2)
        self.assertEqual(tx.status, 'completed')
