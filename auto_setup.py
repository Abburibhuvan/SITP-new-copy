"""
Automatic setup script that runs on deployment
Creates admin user and sets up departments
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TAU.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Department, Profile
from Student.models import SLAConfig, PRIORITY_CHOICES

def setup_admin():
    """Create admin user if it doesn't exist"""
    print("=" * 60)
    print("SETTING UP ADMIN USER")
    print("=" * 60)
    
    admin_username = os.getenv('ADMIN_USERNAME', 'admin')
    admin_password = os.getenv('ADMIN_PASSWORD', 'Admin@2024')
    admin_email = os.getenv('ADMIN_EMAIL', 'admin@apollouniversity.edu')
    
    try:
        admin_user = User.objects.get(username=admin_username)
        print(f"Admin user '{admin_username}' already exists. Updating password...")
        admin_user.set_password(admin_password)
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.email = admin_email
        admin_user.save()
    except User.DoesNotExist:
        print(f"Creating admin user '{admin_username}'...")
        admin_user = User.objects.create_superuser(
            username=admin_username,
            email=admin_email,
            password=admin_password,
            first_name='Admin',
            last_name='User'
        )
    
    # Setup profile
    general_dept, _ = Department.objects.get_or_create(
        name='General',
        defaults={'sla_hours': 24}
    )
    
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
    
    print(f"✓ Admin user created/updated")
    print(f"  Username: {admin_username}")
    print(f"  Password: {admin_password}")
    print(f"  Email: {admin_email}")
    print()

def setup_departments():
    """Create default departments"""
    print("=" * 60)
    print("SETTING UP DEPARTMENTS")
    print("=" * 60)
    
    departments = [
        ('Finance', 48),
        ('Hostel', 48),
        ('Mess', 48),
        ('Academics', 48),
        ('Gate Pass', 24),
        ('General', 24),
    ]
    
    for dept_name, sla_hours in departments:
        dept, created = Department.objects.get_or_create(
            name=dept_name,
            defaults={'sla_hours': sla_hours}
        )
        status = "Created" if created else "Exists"
        print(f"  {status}: {dept_name} (SLA: {sla_hours}h)")
    print()

def setup_sla_configs():
    """Create SLA configurations for all departments"""
    print("=" * 60)
    print("SETTING UP SLA CONFIGURATIONS")
    print("=" * 60)
    
    sla_count = 0
    for dept in Department.objects.all():
        for priority_code, priority_name in PRIORITY_CHOICES:
            # Set different SLA times based on priority
            if priority_code == 'urgent':
                response_hours = 2
                resolution_hours = 8
                escalation_hours = 6
            elif priority_code == 'high':
                response_hours = 4
                resolution_hours = 24
                escalation_hours = 20
            elif priority_code == 'medium':
                response_hours = 8
                resolution_hours = 48
                escalation_hours = 40
            else:  # low
                response_hours = 24
                resolution_hours = 72
                escalation_hours = 60
            
            sla, created = SLAConfig.objects.get_or_create(
                department=dept,
                priority=priority_code,
                defaults={
                    'response_time_hours': response_hours,
                    'resolution_time_hours': resolution_hours,
                    'escalation_time_hours': escalation_hours
                }
            )
            if created:
                sla_count += 1
    
    print(f"  ✓ Created {sla_count} SLA configurations")
    print()

def main():
    """Run all setup tasks"""
    print("\n" + "=" * 60)
    print("AUTOMATIC DEPLOYMENT SETUP")
    print("=" * 60 + "\n")
    
    try:
        setup_admin()
        setup_departments()
        setup_sla_configs()
        
        print("=" * 60)
        print("✓ SETUP COMPLETED SUCCESSFULLY")
        print("=" * 60)
        print("\nYou can now login with:")
        print(f"  Username: {os.getenv('ADMIN_USERNAME', 'admin')}")
        print(f"  Password: {os.getenv('ADMIN_PASSWORD', 'Admin@2024')}")
        print()
        
    except Exception as e:
        print(f"\n✗ ERROR during setup: {str(e)}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    main()
