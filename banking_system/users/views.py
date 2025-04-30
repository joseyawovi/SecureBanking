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
            subject = 'Welcome to LPU FinTrust - Verify Your Email'
            message = f'''
            Dear {user.full_name},
            
            Thank you for choosing LPU FinTrust as your trusted banking partner!
            
            Your verification code is: {verification_code}
            
            Please enter this code on the verification page to complete your registration.
            Once verified, your account details will be sent to this email address.
            
            Best regards,
            LPU FinTrust Team
            '''
            from_email = 'noreply@lpufintrust.com'
            recipient_list = [user.email]
            
            # Print a message to confirm we're sending email to console
            print(f"\n{'*'*80}")
            print(f"SENDING EMAIL TO: {user.email}")
            print(f"FROM: {from_email}")
            print(f"SUBJECT: {subject}")
            print(f"MESSAGE: \n{message}")
            print(f"{'*'*80}\n")
            
            try:
                send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            except Exception as e:
                print(f"Email error: {e}")
                # Continue anyway since we're using console backend
            
            # Login user but restrict access until verified
            login(request, user)
            messages.success(request, 'Registration successful! Please verify your email address. The verification code has been printed to the console.')
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
                user = request.user
                user.is_verified = True
                user.verification_code = None
                user.save()
                
                # Send account details email
                account = user.account
                subject = 'Welcome to LPU FinTrust - Your Account Details'
                message = f'''
                Dear {user.full_name},

                Your account has been successfully verified. Here are your account details:

                Account Number: {account.account_number}
                Account Holder: {user.full_name}
                Initial PIN: {account._generate_pin()}  # This is a one-time generated PIN

                IMPORTANT: Please change your PIN immediately after your first login for security.

                For assistance, contact our support team.

                Best regards,
                LPU FinTrust Team
                '''
                
                print(f"\n{'*'*80}")
                print("SENDING ACCOUNT DETAILS EMAIL")
                print(f"TO: {user.email}")
                print(f"SUBJECT: {subject}")
                print(f"MESSAGE: \n{message}")
                print(f"{'*'*80}\n")
                
                try:
                    send_mail(
                        subject,
                        message,
                        'noreply@lpufintrust.com',
                        [user.email],
                        fail_silently=False
                    )
                except Exception as e:
                    print(f"Email error: {e}")
                
                messages.success(request, 'Email verified successfully! Check your email for account details.')
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
    message = f'''
    Hello {request.user.full_name},
    
    You requested a new verification code.
    
    Your new verification code is: {verification_code}
    
    Please enter this code on the verification page to complete your registration.
    
    Best regards,
    SecureBank Team
    '''
    from_email = 'noreply@securebank.com'
    recipient_list = [request.user.email]
    
    # Print a message to confirm we're sending email to console
    print(f"\n{'*'*80}")
    print(f"RESENDING VERIFICATION EMAIL TO: {request.user.email}")
    print(f"FROM: {from_email}")
    print(f"SUBJECT: {subject}")
    print(f"MESSAGE: \n{message}")
    print(f"{'*'*80}\n")
    
    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
    except Exception as e:
        print(f"Email error: {e}")
        # Continue anyway since we're using console backend
    
    messages.success(request, 'A new verification code has been sent to your email. Please check the console for the verification code.')
    return redirect('users:verify_email')
