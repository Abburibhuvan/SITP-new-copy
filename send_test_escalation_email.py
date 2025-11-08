import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TAU.settings')
django.setup()

from django.contrib.auth import get_user_model
from Student.models import Ticket, Department
from core.utils import send_escalation_notification_to_admins

def create_test_ticket():
    # Get or create a test user
    User = get_user_model()
    student, _ = User.objects.get_or_create(
        username='teststudent',
        defaults={
            'email': '122311510119@apollouniversity.edu.in',
            'first_name': 'Test',
            'last_name': 'Student'
        }
    )
    
    # Get or create a test department
    department, _ = Department.objects.get_or_create(
        name='Test Department',
        defaults={'sla_hours': 24}
    )
    
    # Create a test ticket
    ticket = Ticket.objects.create(
        student=student,
        department=department,
        subject='Test Escalation Email',
        description='This is a test ticket for email escalation',
        status='open',
        priority='medium'
    )
    
    # Update the ticket ID to something recognizable
    ticket.ticket_id = f'TEST-{ticket.ticket_id}'
    ticket.save()
    
    return ticket, student

if __name__ == "__main__":
    print("=== Starting test email sending process ===")
    
    # Create test data
    test_ticket, test_user = create_test_ticket()
    print(f"Created test ticket: {test_ticket.ticket_id}")
    print(f"Sending to: {test_user.email}")
    
    # Send test escalation email
    try:
        print("\nSending test escalation email...")
        send_escalation_notification_to_admins(
            ticket=test_ticket,
            escalated_by=test_user,
            reason="Testing email delivery"
        )
        print("\nTest email sent successfully!")
    except Exception as e:
        print(f"\nError sending test email: {str(e)}")
    
    print("\n=== Test email sending process completed ===")
