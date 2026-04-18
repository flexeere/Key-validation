import re
from django import forms
from django.core.exceptions import ValidationError
from .models import Company

class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'address', 'contact_name', 'email', 'gst_number']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input w-full rounded border-gray-300', 'placeholder': 'e.g. Acme Corp'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea w-full rounded border-gray-300', 'rows': 3}),
            'contact_name': forms.TextInput(attrs={'class': 'form-input w-full rounded border-gray-300'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-full rounded border-gray-300'}),
            'gst_number': forms.TextInput(attrs={'class': 'form-input w-full rounded border-gray-300'}),
        }

    def clean_gst_number(self):
        gst = self.cleaned_data.get('gst_number', '').strip().upper()
        # Basic alphanumeric check for GST format (Indian format assumed: 15 alphanumeric characters)
        if not re.match(r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$', gst):
            if not gst.isalnum():
                raise ValidationError("GST Number should be alphanumeric.")
            # For demonstration and broader flexibility, if strictly 15 isn't met but it's alphanumeric, 
            # we might just warn or let it pass, but typically GST is 15 chars.
            if len(gst) < 10:
                raise ValidationError("GST pattern seems invalid. Must be purely alphanumeric.")
        return gst
