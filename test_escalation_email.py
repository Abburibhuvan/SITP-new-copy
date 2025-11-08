import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TAU.settings')
django.setup()

from django.contrib.auth import get_user_model
from Student.models import Ticket, Department
from core.utils import send_escalation_notification_to_admins

def test_escalation_email():
    """Test function to send an escalation email."""
    print("===== TESTING ESCALATION EMAIL =====")
    
    # Get or create test user
    User = get_user_model()
    student = User.objects.filter(email='122311510119@apollouniversity.edu.in').first()
    
    if not student:
        print("Creating test student...")
        student = User.objects.create_user(
            username='teststudent',
            email='122311510119@apollouniversity.edu.in',
            first_name='Test',
            last_name='Student',
            password='testpassword123'
        )
    
    # Get or create test department
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
    
    # Set a test ticket ID
    ticket.ticket_id = f'TEST-{ticket.id}'
    ticket.original_department = department  # Make sure original_department is set
    ticket.save()
    
    print(f"Created test ticket: {ticket.ticket_id}")
    print(f"Sending to: {student.email}")
    
    # Send test escalation email
    try:
        print("\nSending test escalation email...")
        send_escalation_notification_to_admins(
            ticket=ticket,
            escalated_by=student,  # Using student as the escalator for testing
            reason="Testing escalation email delivery"
        )
        print("\nTest escalation email sent successfully!")
    except Exception as e:
        print(f"\nError sending test email: {str(e)}")
    
    print("\n===== TEST COMPLETED =====")

if __name__ == "__main__":
    test_escalation_email()
