from django.contrib import admin
from django.utils import timezone
from .models import KYCDocument


@admin.register(KYCDocument)
class KYCDocumentAdmin(admin.ModelAdmin):
    list_display = ('user', 'document_type', 'status', 'uploaded_at', 'verified_at')
    list_filter = ('document_type', 'status', 'uploaded_at', 'verified_at')
    search_fields = ('user__email', 'user__full_name', 'document_number')
    readonly_fields = ('document_file', 'uploaded_at')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Document Information', {
            'fields': ('document_type', 'document_number', 'document_file')
        }),
        ('Verification', {
            'fields': ('status', 'rejection_reason', 'verified_at', 'verified_by')
        }),
        ('Timestamps', {
            'fields': ('uploaded_at',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        # Track admin who verifies the document
        if change and 'status' in form.changed_data:
            if obj.status == 'approved' or obj.status == 'rejected':
                obj.verified_by = request.user
                obj.verified_at = timezone.now()
        
        super().save_model(request, obj, form, change)
