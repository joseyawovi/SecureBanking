from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import KYCDocumentForm
from .models import KYCDocument


@login_required
def upload_document(request):
    """
    View for uploading KYC documents
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email before uploading KYC documents.')
        return redirect('users:verify_email')
    
    if request.method == 'POST':
        form = KYCDocumentForm(request.POST, request.FILES)
        if form.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()
            messages.success(request, 'Document uploaded successfully. It is now pending verification.')
            return redirect('kyc:kyc_status')
    else:
        form = KYCDocumentForm()
    
    return render(request, 'kyc/upload_documents.html', {'form': form})


@login_required
def kyc_status(request):
    """
    View for checking KYC status
    """
    if not request.user.is_verified:
        messages.warning(request, 'Please verify your email to view your KYC status.')
        return redirect('users:verify_email')
    
    documents = KYCDocument.objects.filter(user=request.user).order_by('-uploaded_at')
    
    # Determine overall KYC status
    kyc_status = 'Not Started'
    if documents.exists():
        if documents.filter(status='approved').exists():
            kyc_status = 'Approved'
        elif documents.filter(status='pending').exists():
            kyc_status = 'Pending'
        else:
            kyc_status = 'Rejected'
    
    context = {
        'documents': documents,
        'kyc_status': kyc_status
    }
    
    return render(request, 'kyc/kyc_status.html', context)
