import os
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def kyc_document_path(instance, filename):
    """Generate a unique file path for each KYC document"""
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('kyc_documents', str(instance.user.id), filename)


class KYCDocument(models.Model):
    """
    Model for KYC document verification
    """
    DOCUMENT_TYPES = (
        ('passport', 'Passport'),
        ('drivers_license', 'Driver\'s License'),
        ('national_id', 'National ID'),
        ('utility_bill', 'Utility Bill'),
    )
    
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='kyc_documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=50)
    document_file = models.FileField(upload_to=kyc_document_path)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    rejection_reason = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='verified_documents'
    )
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'KYC Document'
        verbose_name_plural = 'KYC Documents'
    
    def __str__(self):
        return f"{self.get_document_type_display()} - {self.user.email}"
    
    def save(self, *args, **kwargs):
        # Set verified_at if status changes to approved or rejected
        if self.pk:
            old_status = KYCDocument.objects.get(pk=self.pk).status
            if old_status != self.status and self.status in ['approved', 'rejected']:
                self.verified_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def is_verified(self):
        return self.status == 'approved'
    
    @property
    def filename(self):
        return os.path.basename(self.document_file.name)
