import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TAU.settings')
django.setup()

from Student.models import Ticket, Department
from django.contrib.auth.models import User

# Quick test
ticket = Ticket.objects.filter(status='open').first()
if ticket:
    admin = User.objects.filter(is_staff=True).first()
    if admin:
        print(f"Testing escalation for ticket {ticket.ticket_id}")
        print(f"Student email: {ticket.student.email}")
        ticket.escalate(admin, "Quick test escalation")
        print("Escalation completed!")
    else:
        print("No admin user found")
else:
    print("No open tickets found")