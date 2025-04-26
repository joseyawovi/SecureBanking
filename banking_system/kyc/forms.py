from django import forms
from .models import KYCDocument


class KYCDocumentForm(forms.ModelForm):
    """
    Form for uploading KYC documents
    """
    class Meta:
        model = KYCDocument
        fields = ['document_type', 'document_number', 'document_file']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-control'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your document number'}),
            'document_file': forms.FileInput(attrs={'class': 'form-control'})
        }
    
    def clean_document_file(self):
        document_file = self.cleaned_data.get('document_file')
        
        # Check file size (max 5MB)
        if document_file and document_file.size > 5 * 1024 * 1024:
            raise forms.ValidationError("File size must be less than 5MB")
        
        # Check file extension
        if document_file:
            ext = document_file.name.split('.')[-1].lower()
            if ext not in ['pdf', 'png', 'jpg', 'jpeg']:
                raise forms.ValidationError("Only PDF, PNG, JPG, or JPEG files are allowed")
        
        return document_file


class KYCVerificationForm(forms.ModelForm):
    """
    Form for admin to verify KYC documents
    """
    class Meta:
        model = KYCDocument
        fields = ['status', 'rejection_reason']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'rejection_reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
        }
    
    def clean(self):
        cleaned_data = super().clean()
        status = cleaned_data.get('status')
        rejection_reason = cleaned_data.get('rejection_reason')
        
        if status == 'rejected' and not rejection_reason:
            self.add_error('rejection_reason', "Rejection reason is required when rejecting a document")
        
        return cleaned_data
