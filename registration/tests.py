from django.test import TestCase, Client
from django.urls import reverse
from django.core import mail
from .models import Company, ValidationKey
from datetime import timedelta
from django.utils import timezone

class RegistrationTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register_company')

    def test_company_creation_and_key_generation(self):
        """Test Company creation automatically creates a ValidationKey."""
        company = Company.objects.create(
            name="Test Corp",
            address="123 Test St",
            contact_name="John Doe",
            email="test@example.com",
            gst_number="12ABCDE3456F7Z8"
        )
        self.assertTrue(hasattr(company, 'validation_key'))
        self.assertIsNotNone(company.validation_key.token)
        self.assertEqual(company.is_verified, False)
        self.assertFalse(company.validation_key.is_used)

    def test_registration_view(self):
        """Test the registration form submission and email dispatch."""
        data = {
            'name': 'View Test Corp',
            'address': '456 View Blvd',
            'contact_name': 'Jane Doe',
            'email': 'jane@example.com',
            'gst_number': '99ZZZZZ9999Z9Z9'
        }
        response = self.client.post(self.register_url, data)
        
        # Should render the success page without redirect if coded as return render
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Company.objects.filter(email='jane@example.com').exists())
        
        # Test if email actually got queued into Django's outbox
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Verify Your Company Portal Registration', mail.outbox[0].subject)

    def test_verification_valid_key(self):
        """Test clicking a valid email key link activates the profile."""
        company = Company.objects.create(
            name="Valid Corp",
            address="Line 1",
            contact_name="Bob",
            email="bob@example.com",
            gst_number="11AAAAA1111A1A1"
        )
        key = company.validation_key.token
        
        verify_url = reverse('verify_email', args=[key])
        response = self.client.get(verify_url)
        
        self.assertEqual(response.status_code, 200)
        
        # Refresh from db
        company.refresh_from_db()
        self.assertTrue(company.is_verified)
        self.assertTrue(company.validation_key.is_used)

    def test_verification_expired_key(self):
        """Test expired key scenario."""
        company = Company.objects.create(
            name="Expired Corp",
            address="Line 1",
            contact_name="Alice",
            email="alice@example.com",
            gst_number="22BBBBB2222B2B2"
        )
        val_key = company.validation_key
        # Forcibly expire
        val_key.expires_at = timezone.now() - timedelta(hours=1)
        val_key.save()

        verify_url = reverse('verify_email', args=[val_key.token])
        response = self.client.get(verify_url)
        
        # Still 200 because we render an error page
        self.assertEqual(response.status_code, 200)
        
        company.refresh_from_db()
        self.assertFalse(company.is_verified)
