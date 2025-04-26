from django.test import TestCase
from django.urls import reverse
from .models import User


class UserModelTests(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='testuser@example.com',
            full_name='Test User',
            password='testpassword123'
        )
        self.assertEqual(user.email, 'testuser@example.com')
        self.assertEqual(user.full_name, 'Test User')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_verified)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            full_name='Admin User',
            password='adminpassword123'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertEqual(admin_user.full_name, 'Admin User')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        self.assertTrue(admin_user.is_verified)


class UserRegistrationTests(TestCase):
    def test_registration_view(self):
        response = self.client.get(reverse('users:register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_user_registration(self):
        response = self.client.post(reverse('users:register'), {
            'email': 'newuser@example.com',
            'full_name': 'New User',
            'password1': 'securepass123',
            'password2': 'securepass123',
        })
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.first().email, 'newuser@example.com')
        self.assertRedirects(response, reverse('users:verify_email'))


class UserLoginTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            full_name='Test User',
            password='testpassword123',
            is_verified=True
        )

    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_login_success(self):
        response = self.client.post(reverse('users:login'), {
            'username': 'testuser@example.com',
            'password': 'testpassword123',
        })
        self.assertRedirects(response, reverse('dashboard:user_dashboard'))
