from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from .models import User


class CustomUserCreationForm(UserCreationForm):
    """
    Form for user registration with custom fields
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-lg border-gray-300 focus:border-primary-500 focus:ring-primary-500',
            'placeholder': 'Enter your email address'
        })
    )
    full_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border-gray-300 focus:border-primary-500 focus:ring-primary-500',
            'placeholder': 'Enter your full name'
        })
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border-gray-300 focus:border-primary-500 focus:ring-primary-500',
            'placeholder': 'Enter your phone number (optional)'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border-gray-300 focus:border-primary-500 focus:ring-primary-500',
            'placeholder': 'Create a strong password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border-gray-300 focus:border-primary-500 focus:ring-primary-500',
            'placeholder': 'Confirm your password'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone_number', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email


class CustomAuthenticationForm(AuthenticationForm):
    """
    Form for user login with custom styling
    """
    username = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full rounded-lg border-gray-300 focus:border-primary-500 focus:ring-primary-500',
            'placeholder': 'Enter your email address'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border-gray-300 focus:border-primary-500 focus:ring-primary-500',
            'placeholder': 'Enter your password'
        })
    )


class EmailVerificationForm(forms.Form):
    """
    Form for email verification code
    """
    verification_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border-gray-300 focus:border-primary-500 focus:ring-primary-500',
            'placeholder': 'Enter the verification code sent to your email'
        })
    )
