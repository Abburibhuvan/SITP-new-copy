import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TAU.settings')
django.setup()

from Student.models import Ticket
from django.contrib.auth import get_user_model
from core.utils import send_escalation_notification_to_admins

def main():
    print("===== DIRECT ESCALATION EMAIL TEST =====")
    
    # Get the first available ticket and user
    User = get_user_model()
    
    # Try to get a ticket that exists
    ticket = Ticket.objects.first()
    if not ticket:
        print("No tickets found in the database.")
        return
    
    # Get a user to be the escalator
    user = User.objects.first()
    if not user:
        print("No users found in the database.")
        return
    
    print(f"Using ticket: {ticket.ticket_id}")
    print(f"Student email: {ticket.student.email}")
    print(f"Escalated by: {user.get_full_name()} ({user.email})")
    
    # Make sure the ticket has an original_department
    if not ticket.original_department:
        ticket.original_department = ticket.department
        ticket.save()
        print(f"Set original_department to: {ticket.original_department.name}")
    
    # Send the escalation email
    print("\nSending escalation notification...")
    try:
        send_escalation_notification_to_admins(
            ticket=ticket,
            escalated_by=user,
            reason="Testing direct escalation email"
        )
        print("\nEscalation notification sent successfully!")
    except Exception as e:
        print(f"\nError sending escalation notification: {str(e)}")
    
    print("\n===== TEST COMPLETED =====")

if __name__ == "__main__":
    main()
