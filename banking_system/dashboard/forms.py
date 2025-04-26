from django import forms
from kyc.models import KYCDocument


class AdminKYCVerificationForm(forms.ModelForm):
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
