import secrets
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Company(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    contact_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    gst_number = models.CharField(max_length=50, unique=True, db_index=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return f"{self.name} - {self.gst_number}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            ValidationKey.objects.create(company=self)

class ValidationKey(models.Model):
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name='validation_key')
    token = models.CharField(max_length=128, unique=True, db_index=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def generate_token(self):
        if not self.token:
            # Generate a cryptographically secure URL-safe token
            self.token = secrets.token_urlsafe(64)
    
    def set_expiration(self):
        if not self.expires_at:
            # Set lifespan to 48 hours
            self.expires_at = timezone.now() + timedelta(hours=48)

    def save(self, *args, **kwargs):
        self.generate_token()
        self.set_expiration()
        super().save(*args, **kwargs)

    def is_valid(self):
        return not self.is_used and self.expires_at > timezone.now()

    def __str__(self):
        return f"Key for {self.company.name}"
