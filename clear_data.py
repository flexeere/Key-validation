import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from registration.models import Company

# Delete all companies, which will cascade and delete ValidationKeys
deleted_count, _ = Company.objects.all().delete()
print(f"Successfully deleted {deleted_count} Company records.")
