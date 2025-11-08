#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TAU.settings')
django.setup()

from Student.models import Ticket, Department
from django.contrib.auth.models import User
from django.utils import timezone
from dept_admin.views import escalate_ticket
from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage

def test_ui_escalation():
    print("Testing UI escalation process...")
    
    # Get a test ticket
    try:
        ticket = Ticket.objects.filter(status='open').first()
        if not ticket:
            print("No open tickets found. Creating a test ticket...")
            # Create a test department if needed
            dept, _ = Department.objects.get_or_create(name='Test Department', defaults={'sla_hours': 24})
            
            # Create a test user if needed
            user, _ = User.objects.get_or_create(
                username='test_student',
                defaults={
                    'email': 'test@apollouniversity.edu.in',
                    'first_name': 'Test',
                    'last_name': 'Student'
                }
            )
            
            # Create a test ticket
            ticket = Ticket.objects.create(
                student=user,
                department=dept,
                subject='Test Ticket for UI Escalation',
                description='This is a test ticket to test UI escalation functionality',
                priority='medium',
                status='open'
            )
            print(f"Created test ticket: {ticket.ticket_id}")
        
        print(f"Testing UI escalation for ticket: {ticket.ticket_id}")
        print(f"Current status: {ticket.status}")
        print(f"Student email: {ticket.student.email}")
        
        # Get a test admin user
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            print("No admin user found. Creating one...")
            admin_user = User.objects.create_user(
                username='test_admin',
                email='admin@test.com',
                password='testpass123',
                is_staff=True
            )
        
        print(f"Using admin user: {admin_user.username}")
        
        # Create a mock request to simulate the UI escalation
        factory = RequestFactory()
        request = factory.post(f'/department/escalate-ticket/{ticket.id}/', {
            'reason': 'Test escalation from UI simulation'
        })
        
        # Set up the request user and messages
        request.user = admin_user
        setattr(request, 'session', {})
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        
        print("Simulating UI escalation request...")
        
        # Call the escalate_ticket view
        from django.shortcuts import get_object_or_404
        from dept_admin.decorators import dept_admin_required
        
        # We need to mock the department admin requirement
        def mock_dept_admin_required(view_func):
            return view_func
        
        # Temporarily replace the decorator
        import dept_admin.views
        original_decorator = dept_admin.views.dept_admin_required
        dept_admin.views.dept_admin_required = mock_dept_admin_required
        
        try:
            response = escalate_ticket(request, ticket.id)
            print(f"View response: {response}")
        except Exception as e:
            print(f"Error during UI escalation simulation: {e}")
            import traceback
            traceback.print_exc()
        finally:
            # Restore the original decorator
            dept_admin.views.dept_admin_required = original_decorator
        
        # Check the ticket status after escalation
        ticket.refresh_from_db()
        print(f"Ticket status after UI escalation: {ticket.status}")
        print(f"Escalated at: {ticket.escalated_at}")
        print(f"Escalated by: {ticket.escalated_by}")
        print(f"Escalation reason: {ticket.escalation_reason}")
        
    except Exception as e:
        print(f"Error during UI escalation test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_ui_escalation()