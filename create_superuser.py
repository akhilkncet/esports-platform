import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'esports_platform.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@esports.com',
        password='admin123',
        is_organizer=True
    )
    print("✓ Superuser created successfully!")
    print("  Username: admin")
    print("  Password: admin123")
    print("  Email: admin@esports.com")
else:
    print("✓ Superuser already exists")
