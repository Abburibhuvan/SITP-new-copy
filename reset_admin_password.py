import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TAU.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Department, Profile

# Get or create admin user
admin_user, created = User.objects.get_or_create(
    username='admin',
    defaults={
        'email': 'admin@apollouniversity.edu',
        'is_staff': True,
        'is_superuser': True,
        'first_name': 'Admin',
        'last_name': 'User'
    }
)

# Set password
new_password = 'Admin@2024'
admin_user.set_password(new_password)
admin_user.is_staff = True
admin_user.is_superuser = True
admin_user.save()

# Get or create General department
general_dept, _ = Department.objects.get_or_create(
    name='General',
    defaults={'sla_hours': 24}
)

# Create or update profile
profile, _ = Profile.objects.get_or_create(
    user=admin_user,
    defaults={
        'department': general_dept,
        'is_admin': True,
        'must_change_password': False
    }
)

if not created:
    profile.department = general_dept
    profile.is_admin = True
    profile.must_change_password = False
    profile.save()

print("=" * 60)
print("ADMIN USER CREDENTIALS")
print("=" * 60)
print(f"Username: admin")
print(f"Password: {new_password}")
print(f"Email: {admin_user.email}")
print(f"Department: {profile.department.name}")
print("=" * 60)
print("\nAdmin user setup complete!")
print("You can login at: http://127.0.0.1:7000/admin/")
print("Or student portal: http://127.0.0.1:7000/")
