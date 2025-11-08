import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TAU.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Department, Profile

# Get or create the General department
general_dept, _ = Department.objects.get_or_create(
    name='General',
    defaults={'sla_hours': 24}
)

# Get the admin user
admin_user = User.objects.filter(username='admin').first()

if admin_user:
    # Create or update their profile
    profile, created = Profile.objects.get_or_create(
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
    
    # Set password
    admin_user.set_password('admin123')
    admin_user.save()
    
    print(f"Successfully set up {admin_user.username} as General department admin")
    print(f"Username: admin")
    print(f"Password: admin123")
else:
    print("Admin user not found")
