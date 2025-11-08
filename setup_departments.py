import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TAU.settings')
django.setup()

from core.models import Department
from Student.models import SLAConfig, PRIORITY_CHOICES

# Create default departments
departments = [
    ('Finance', 48),
    ('Hostel', 48),
    ('Mess', 48),
    ('Academics', 48),
    ('Gate Pass', 24),
    ('General', 24),
]

print("Setting up departments...")
for dept_name, sla_hours in departments:
    dept, created = Department.objects.get_or_create(
        name=dept_name,
        defaults={'sla_hours': sla_hours}
    )
    if created:
        print(f"  Created: {dept_name} (SLA: {sla_hours}h)")
    else:
        print(f"  Exists: {dept_name} (SLA: {dept.sla_hours}h)")

# Create SLA configurations for each department and priority
print("\nSetting up SLA configurations...")
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
            print(f"  Created SLA: {dept.name} - {priority_name} (Response: {response_hours}h, Resolution: {resolution_hours}h)")

print("\nSetup complete!")
