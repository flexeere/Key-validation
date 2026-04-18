import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'CodeX2026!')
    print("Created superuser 'admin'")
else:
    u = User.objects.get(username='admin')
    u.set_password('CodeX2026!')
    u.save()
    print("Reset password for superuser 'admin'")
