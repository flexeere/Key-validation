from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from .forms import CompanyRegistrationForm
from .models import ValidationKey

class RegisterCompanyView(View):
    def get(self, request):
        form = CompanyRegistrationForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = CompanyRegistrationForm(request.POST)
        if form.is_valid():
            company = form.save()
            key = company.validation_key
            
            # Construct Validation URL dynamically
            verify_url = request.build_absolute_uri(reverse('verify_email', args=[key.token]))
            
            # Dispatch email containing token
            self.dispatch_email(company, verify_url)
            
            return render(request, 'registration/registration_sent.html', {'email': company.email})
            
        return render(request, 'registration/register.html', {'form': form})

    def dispatch_email(self, company, url):
        """Helper function pointing to the sync email dispatcher"""
        subject = 'Verify Your Company Portal Registration'
        message = f"""
Hello {company.contact_name},

Thank you for registering {company.name}. 
Please use the secure link below to validate your account:

{url}

This link will expire in 48 hours.

Regards,
Registration Team
"""
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.SERVER_EMAIL if hasattr(settings, 'SERVER_EMAIL') else 'noreply@flexeere.com',
            recipient_list=[company.email],
            fail_silently=False,
        )


class VerifyKeyView(View):
    def get(self, request, token):
        # Fetch the token utilizing the database index
        # For secure operations, avoiding manual ObjectDoesNotExist exceptions with get_object_or_404
        try:
            val_key = ValidationKey.objects.get(token=token)
        except ValidationKey.DoesNotExist:
            return render(request, 'registration/verification_failed.html', {'error': 'Invalid or missing key.'})

        if not val_key.is_valid():
            return render(request, 'registration/verification_failed.html', {'error': 'This verification link has expired or has already been used.'})

        # Process valid token
        val_key.is_used = True
        val_key.save()

        company = val_key.company
        company.is_verified = True
        company.save()

        return render(request, 'registration/verification_success.html', {'company': company})
