from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from users.models import User
from accounts.models import Account
from cards.models import Card
from kyc.models import KYCDocument
from transactions.models import Transaction
from .forms import AdminKYCVerificationForm


@login_required
def user_dashboard(request):
    """
    User dashboard showing account info, balance, recent transactions, KYC status and cards
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to access your dashboard.')
        return redirect('users:verify_email')
    
    # Get user's account
    account = request.user.account
    
    # Get recent transactions
    recent_transactions = Transaction.objects.filter(
        account=account
    ) | Transaction.objects.filter(
        recipient_account=account
    )
    recent_transactions = recent_transactions.order_by('-timestamp')[:5]
    
    # Get user's cards
    cards = Card.objects.filter(user=request.user, is_active=True)
    
    # Get KYC status
    kyc_documents = KYCDocument.objects.filter(user=request.user).order_by('-uploaded_at')
    kyc_status = 'Not Started'
    if kyc_documents.exists():
        if kyc_documents.filter(status='approved').exists():
            kyc_status = 'Approved'
        elif kyc_documents.filter(status='pending').exists():
            kyc_status = 'Pending'
        else:
            kyc_status = 'Rejected'
    
    context = {
        'account': account,
        'recent_transactions': recent_transactions,
        'cards': cards,
        'kyc_documents': kyc_documents,
        'kyc_status': kyc_status,
    }
    
    return render(request, 'dashboard/user_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    """
    Admin dashboard showing pending KYC submissions, user info, and system logs
    """
    # Get pending KYC documents
    pending_kyc = KYCDocument.objects.filter(status='pending').order_by('-uploaded_at')
    
    # Get recent users
    recent_users = User.objects.order_by('-date_joined')[:10]
    
    # Get recent transactions
    recent_transactions = Transaction.objects.order_by('-timestamp')[:10]
    
    # Get system stats
    total_users = User.objects.count()
    total_accounts = Account.objects.count()
    total_active_accounts = Account.objects.filter(is_active=True).count()
    total_transactions = Transaction.objects.count()
    total_cards = Card.objects.count()
    
    context = {
        'pending_kyc': pending_kyc,
        'recent_users': recent_users,
        'recent_transactions': recent_transactions,
        'total_users': total_users,
        'total_accounts': total_accounts,
        'total_active_accounts': total_active_accounts,
        'total_transactions': total_transactions,
        'total_cards': total_cards,
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)


@login_required
@user_passes_test(lambda u: u.is_staff)
def verify_kyc_document(request, document_id):
    """
    Admin view to verify a KYC document
    """
    document = get_object_or_404(KYCDocument, id=document_id)
    
    if request.method == 'POST':
        form = AdminKYCVerificationForm(request.POST, instance=document)
        if form.is_valid():
            kyc_doc = form.save(commit=False)
            kyc_doc.verified_by = request.user
            kyc_doc.verified_at = timezone.now()
            kyc_doc.save()
            
            status = kyc_doc.get_status_display().lower()
            messages.success(request, f'Document has been {status} successfully.')
            return redirect('dashboard:admin_dashboard')
    else:
        form = AdminKYCVerificationForm(instance=document)
    
    return render(request, 'dashboard/verify_kyc_document.html', {
        'form': form,
        'document': document
    })
