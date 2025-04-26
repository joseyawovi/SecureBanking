from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import Account
from transactions.models import Transaction
from cards.models import Card
from decimal import Decimal

User = get_user_model()


class DashboardViewTests(TestCase):
    def setUp(self):
        # Create a verified user
        self.user = User.objects.create_user(
            email='testuser@example.com',
            full_name='Test User',
            password='testpassword123',
            is_verified=True
        )
        
        # Get the user's account
        self.account = Account.objects.get(user=self.user)
        
        # Create a card for the user
        self.card = Card.objects.create(
            user=self.user,
            card_type='debit',
            balance=Decimal('100.00')
        )
        
        # Create a transaction for the user
        self.transaction = Transaction.create_deposit(
            self.account,
            Decimal('500.00'),
            'Initial deposit'
        )
        
        # Create an admin user
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            full_name='Admin User',
            password='adminpassword123'
        )
    
    def test_user_dashboard_access(self):
        """Test user dashboard is accessible for verified users"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(reverse('dashboard:user_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/user_dashboard.html')
    
    def test_admin_dashboard_access(self):
        """Test admin dashboard is accessible only for admin users"""
        # Regular user should not access admin dashboard
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(reverse('dashboard:admin_dashboard'))
        self.assertEqual(response.status_code, 403)  # Forbidden
        
        # Admin user should access admin dashboard
        self.client.login(email='admin@example.com', password='adminpassword123')
        response = self.client.get(reverse('dashboard:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard/admin_dashboard.html')
    
    def test_user_dashboard_content(self):
        """Test user dashboard contains expected content"""
        self.client.login(email='testuser@example.com', password='testpassword123')
        response = self.client.get(reverse('dashboard:user_dashboard'))
        
        # Check account info is in context
        self.assertIn('account', response.context)
        self.assertEqual(response.context['account'], self.account)
        
        # Check transactions are in context
        self.assertIn('recent_transactions', response.context)
        self.assertEqual(list(response.context['recent_transactions']), [self.transaction])
        
        # Check cards are in context
        self.assertIn('cards', response.context)
        self.assertEqual(list(response.context['cards']), [self.card])
