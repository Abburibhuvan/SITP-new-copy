#!/usr/bin/env python
"""
Test script to verify email functionality
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from core.utils import send_student_email_via_brevo_api

def test_email():
    """Test the email functionality"""
    print("Testing email functionality...")
    
    # Test email
    subject = "Test Email - Escalation System"
    message = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
            .container { max-width: 600px; margin: 0 auto; padding: 20px; }
            .header { background-color: #1E40AF; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }
            .content { padding: 20px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 0 0 5px 5px; }
            .footer { text-align: center; margin-top: 20px; font-size: 12px; color: #666; }
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h1>Test Email</h1>
            </div>
            <div class='content'>
                <p>This is a test email to verify that the escalation email system is working properly.</p>
                <p>If you receive this email, the Brevo API integration is functioning correctly.</p>
                <p>Best regards,<br>Apollo University Support System</p>
            </div>
            <div class='footer'>
                <p>This is a test message.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Replace with a real email address for testing
    test_email = "test@example.com"  # Change this to a real email address
    
    print(f"Sending test email to: {test_email}")
    result = send_student_email_via_brevo_api(subject, message, test_email)
    
    if result:
        print("✅ Email sent successfully!")
    else:
        print("❌ Email sending failed!")
    
    return result

if __name__ == "__main__":
    test_email() 