from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from .models import KYCDocument

User = get_user_model()


class KYCDocumentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='testuser@example.com',
            full_name='Test User',
            password='testpassword123'
        )
        
        # Create a simple PDF file for testing
        self.sample_file = SimpleUploadedFile(
            "test_document.pdf",
            b"file_content",
            content_type="application/pdf"
        )
    
    def test_kyc_document_creation(self):
        """Test KYC document creation and status management"""
        document = KYCDocument.objects.create(
            user=self.user,
            document_type='passport',
            document_number='AB123456',
            document_file=self.sample_file
        )
        
        self.assertEqual(document.status, 'pending')
        self.assertFalse(document.is_verified)
        self.assertIsNone(document.verified_at)
        self.assertIsNone(document.verified_by)
        
        # Test status changes
        document.status = 'approved'
        document.save()
        self.assertTrue(document.is_verified)
        self.assertIsNotNone(document.verified_at)
