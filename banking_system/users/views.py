import random
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm, EmailVerificationForm
from .models import User


def register(request):
    """
    View for user registration
    """
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_verified = False
            verification_code = user.generate_verification_code()
            user.save()
            
            # Send verification email (using console backend for development)
            subject = 'Verify your email address'
            message = f'Your verification code is: {verification_code}'
            from_email = 'noreply@bankingsystem.com'
            recipient_list = [user.email]
            
            send_mail(subject, message, from_email, recipient_list)
            
            # Login user but restrict access until verified
            login(request, user)
            messages.success(request, 'Registration successful! Please verify your email address.')
            return redirect('users:verify_email')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """
    View for user login
    """
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_verified:
                messages.warning(request, 'Please verify your email to fully access your account.')
                login(request, user)
                return redirect('users:verify_email')
            
            login(request, user)
            messages.success(request, f'Welcome back, {user.full_name}!')
            return redirect('dashboard:user_dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def verify_email(request):
    """
    View for email verification
    """
    if request.user.is_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('dashboard:user_dashboard')
    
    if request.method == 'POST':
        form = EmailVerificationForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data['verification_code']
            if code == request.user.verification_code:
                request.user.is_verified = True
                request.user.verification_code = None
                request.user.save()
                messages.success(request, 'Email verified successfully!')
                return redirect('dashboard:user_dashboard')
            else:
                messages.error(request, 'Invalid verification code. Please try again.')
    else:
        form = EmailVerificationForm()
    
    return render(request, 'users/verify_email.html', {'form': form})


@login_required
def resend_verification(request):
    """
    View to resend verification code
    """
    if request.user.is_verified:
        messages.info(request, 'Your email is already verified.')
        return redirect('dashboard:user_dashboard')
    
    # Generate new verification code
    verification_code = request.user.generate_verification_code()
    
    # Send verification email
    subject = 'Verify your email address'
    message = f'Your new verification code is: {verification_code}'
    from_email = 'noreply@bankingsystem.com'
    recipient_list = [request.user.email]
    
    send_mail(subject, message, from_email, recipient_list)
    
    messages.success(request, 'A new verification code has been sent to your email.')
    return redirect('users:verify_email')
