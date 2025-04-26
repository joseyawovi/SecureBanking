import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banking_system.settings')
django.setup()

from django.contrib.auth import get_user_model
from users.models import User

# Define admin credentials
admin_email = 'admin@securebank.com'
admin_password = 'Admin@123'
admin_name = 'Admin User'

# Create admin user
try:
    # Check if user already exists
    if not User.objects.filter(email=admin_email).exists():
        user = User.objects.create_superuser(
            email=admin_email,
            password=admin_password,
            full_name=admin_name,
            is_verified=True
        )
        print(f"Superuser created: {admin_email}")
    else:
        user = User.objects.get(email=admin_email)
        user.set_password(admin_password)
        user.is_superuser = True
        user.is_staff = True
        user.is_verified = True
        user.save()
        print(f"Superuser updated: {admin_email}")
    
    print("Admin credentials:")
    print(f"Email: {admin_email}")
    print(f"Password: {admin_password}")
    print("You can now login to the admin panel at /admin/")
    
except Exception as e:
    print(f"Error creating superuser: {e}")