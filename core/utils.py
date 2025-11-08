from Student.models import Ticket
from datetime import timedelta, datetime
from django.core.mail import send_mail
import requests
import os

def generate_ticket_id(department_name):
    prefix = department_name[:3].upper()
    count = Ticket.objects.filter(department__name=department_name).count() + 1
    return f"AU-2025-{prefix}-{count:04d}"

def calculate_sla_due():
    return datetime.now() + timedelta(days=2)

def send_student_email(subject, message, recipient_email, html_message=None):
    """Send an email to a student using Brevo API."""
    return send_student_email_via_brevo_api(subject, message, recipient_email)

def send_student_email_via_brevo_api(subject, message, recipient_email):
    """Send an email using Brevo's HTTP API as a fallback if SMTP is blocked."""
    api_url = 'https://api.brevo.com/v3/smtp/email'
    # Get API key from environment variable
    api_key = os.getenv('BREVO_API_KEY')
    
    # Log API key status (masked for security)
    api_key_display = f"{api_key[:8]}...{api_key[-4:] if api_key else ''}" if api_key else "[NOT SET]"
    print(f"[DEBUG] Using Brevo API key: {api_key_display}", flush=True)
    
    headers = {
        'accept': 'application/json',
        'api-key': api_key,
        'content-type': 'application/json',
    }
    
    sender_email = "testcasemail019@gmail.com"
    data = {
        "sender": {"name": "TEAM SITP", "email": sender_email},
        "to": [{"email": recipient_email}],
        "subject": subject,
        "htmlContent": message,
    }
    
    try:
        print(f"[DEBUG] ===== SENDING EMAIL VIA BREVO API =====", flush=True)
        print(f"[DEBUG] From: {sender_email}", flush=True)
        print(f"[DEBUG] To: {recipient_email}", flush=True)
        print(f"[DEBUG] Subject: {subject}", flush=True)
        print(f"[DEBUG] API URL: {api_url}", flush=True)
        print(f"[DEBUG] Request Headers: {headers}", flush=True)
        print(f"[DEBUG] Request Data: {data}", flush=True)
        
        # Log the first 200 characters of the message
        print(f"[DEBUG] Email content preview: {message[:200]}...", flush=True)
        
        # Make the API request
        print("[DEBUG] Making API request to Brevo...", flush=True)
        response = requests.post(api_url, headers=headers, json=data, timeout=30)
        
        # Log response details
        print(f"[DEBUG] Response status code: {response.status_code}", flush=True)
        print(f"[DEBUG] Response headers: {dict(response.headers)}", flush=True)
        print(f"[DEBUG] Response content: {response.text}", flush=True)
        
        if response.status_code == 201:
            print(f"[SUCCESS] Email sent successfully to {recipient_email}", flush=True)
            return True
        else:
            error_msg = f"[ERROR] Failed to send email to {recipient_email}. Status: {response.status_code}"
            print(error_msg, flush=True)
            try:
                error_data = response.json()
                print(f"[ERROR] Brevo API error details: {error_data}", flush=True)
            except:
                print(f"[ERROR] Could not parse error response: {response.text}", flush=True)
            return False
            
    except requests.exceptions.Timeout as e:
        error_msg = f"[ERROR] Timeout while sending email to {recipient_email}: {str(e)}"
        print(error_msg, flush=True)
        return False
    except requests.exceptions.RequestException as e:
        error_msg = f"[ERROR] Request exception while sending email to {recipient_email}: {str(e)}"
        print(error_msg, flush=True)
        return False
    except Exception as e:
        error_msg = f"[ERROR] Unexpected error while sending email to {recipient_email}: {str(e)}"
        print(error_msg, flush=True)
        return False
    finally:
        print("[DEBUG] ===== EMAIL SENDING PROCESS COMPLETED =====\n", flush=True)

def send_status_notification(ticket):
    # Compose a professional, mobile-friendly HTML email for ticket update
    attachment_html = ""
    if hasattr(ticket, 'attachment') and ticket.attachment:
        attachment_html = f"""
        <tr>
          <td style='color:#333; padding:8px 0;'><b>Attachment:</b></td>
          <td style='color:#333; padding:8px 0;'><a href='{ticket.attachment.url}' style='color:#1E40AF; text-decoration:underline;'>Download File</a></td>
        </tr>
        """
    else:
        attachment_html = f"""
        <tr>
          <td style='color:#333; padding:8px 0;'><b>Attachment:</b></td>
          <td style='color:#333; padding:8px 0;'>No file attached</td>
        </tr>
        """
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #1E40AF; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ padding: 20px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 0 0 5px 5px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            table.details {{ width: 100%; margin: 20px 0; background: #fff; border-radius: 8px; border: 1px solid #eee; }}
            table.details td {{ padding: 8px 0; }}
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h1>Ticket Status Update</h1>
            </div>
            <div class='content'>
                <p>Dear {ticket.student.first_name},</p>
                <p>We would like to inform you about an update to your ticket <b>#{ticket.ticket_id}</b>:</p>
                <table class='details'>
                    <tr><td><b>Ticket ID:</b></td><td>{ticket.ticket_id}</td></tr>
                    <tr><td><b>Department:</b></td><td>{ticket.department.name}</td></tr>
                    <tr><td><b>Issue:</b></td><td>{ticket.subject}</td></tr>
                    <tr><td><b>Status:</b></td><td>{ticket.status.capitalize()}</td></tr>
                    <tr><td><b>Description:</b></td><td>{ticket.description}</td></tr>
                    {attachment_html}
                </table>
                <p>You can view the full details of your ticket by clicking the button below:</p>
                <p style='text-align:center;'>
                    <a href='https://apollouniversity.edu.in/tickets/{ticket.ticket_id}' style='display:inline-block; padding:10px 20px; background-color:#1E40AF; color:white; text-decoration:none; border-radius:5px;'>View Ticket</a>
                </p>
                <p>If you have any questions or need further assistance, please don't hesitate to contact our support team.</p>
                <p>Best regards,<br>The Support Team<br>Apollo University</p>
            </div>
            <div class='footer'>
                <p>This is an automated message, please do not reply to this email.</p>
                <p>&copy; {datetime.now().year} Apollo University. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    send_student_email_via_brevo_api(
        subject=f"Ticket #{ticket.ticket_id} Status Update: {ticket.status}",
        message=html_message,
        recipient_email=ticket.student.email
    )

def send_ticket_creation_email(ticket):
    html_message = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #1E40AF; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ padding: 20px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 0 0 5px 5px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            table.details {{ width: 100%; margin: 20px 0; background: #fff; border-radius: 8px; border: 1px solid #eee; }}
            table.details td {{ padding: 8px 0; }}
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h1>Ticket Created Successfully</h1>
            </div>
            <div class='content'>
                <p>Hello {ticket.student.first_name},</p>
                <p>Your ticket has been created successfully with the following details:</p>
                <table class='details'>
                    <tr><td><b>Ticket ID:</b></td><td>{ticket.ticket_id}</td></tr>
                    <tr><td><b>Department:</b></td><td>{ticket.department.name}</td></tr>
                    <tr><td><b>Subject:</b></td><td>{ticket.subject}</td></tr>
                    <tr><td><b>Description:</b></td><td>{ticket.description}</td></tr>
                </table>
                <p>You can view your ticket status at any time by logging into the portal.</p>
                <p>Regards,<br>Apollo University Support Team</p>
            </div>
            <div class='footer'>
                <p>This is an automated message, please do not reply to this email.</p>
                <p>&copy; {datetime.now().year} Apollo University. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    send_student_email_via_brevo_api(
        subject=f"Ticket Created: {ticket.ticket_id}",
        message=html_message,
        recipient_email=ticket.student.email
    )

def send_escalation_notification_to_admins(ticket, escalated_by, reason):
    """Send escalation notification to department admins, general support, and the student."""
    print(f"[DEBUG] ===== SENDING ESCALATION NOTIFICATIONS =====", flush=True)
    print(f"[DEBUG] Ticket ID: {ticket.ticket_id}", flush=True)
    print(f"[DEBUG] Student: {ticket.student.get_full_name()} <{ticket.student.email}>", flush=True)
    print(f"[DEBUG] Escalated by: {escalated_by}", flush=True)
    print(f"[DEBUG] Reason: {reason}", flush=True)
    
    # First, notify the student
    student_email = ticket.student.email
    print(f"[DEBUG] Preparing to notify student at: {student_email}", flush=True)
    student_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #1E40AF; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ padding: 20px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 0 0 5px 5px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            table.details {{ width: 100%; margin: 20px 0; background: #fff; border-radius: 8px; border: 1px solid #eee; }}
            table.details td {{ padding: 8px 0; }}
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h1>Ticket Escalated</h1>
            </div>
            <div class='content'>
                <p>Dear {ticket.student.get_full_name() or 'Student'},</p>
                <p>Your ticket has been escalated to ensure it receives proper attention and timely resolution.</p>
                <table class='details'>
                    <tr><td><b>Ticket ID:</b></td><td>{ticket.ticket_id}</td></tr>
                    <tr><td><b>Subject:</b></td><td>{ticket.subject}</td></tr>
                    <tr><td><b>Department:</b></td><td>{ticket.department.name}</td></tr>
                    <tr><td><b>Status:</b></td><td>Escalated to General Support</td></tr>
                    <tr><td><b>Reason:</b></td><td>{reason or 'To ensure timely resolution'}</td></tr>
                    <tr><td><b>Escalated At:</b></td><td>{ticket.escalated_at.strftime('%Y-%m-%d %H:%M:%S') if ticket.escalated_at else 'N/A'}</td></tr>
                </table>
                <p>Our support team will contact you with updates soon. You can also track your ticket status by clicking the button below:</p>
                <p style='text-align:center;'>
                    <a href='https://apollouniversity.edu.in/student/tickets/{ticket.ticket_id}' style='display:inline-block; padding:10px 20px; background-color:#1E40AF; color:white; text-decoration:none; border-radius:5px;'>View Your Ticket</a>
                </p>
                <p>If you have any questions or need further assistance, please don't hesitate to contact our support team.</p>
                <p>Best regards,<br>The Support Team<br>Apollo University</p>
            </div>
            <div class='footer'>
                <p>This is an automated message, please do not reply to this email.</p>
                <p>&copy; {datetime.now().year} Apollo University. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send notification to the student
    try:
        student_email = ticket.student.email
        print(f"[DEBUG] Sending student notification to: {student_email}", flush=True)
        print(f"[DEBUG] Email subject: Update on Your Ticket #{ticket.ticket_id}: Escalated", flush=True)
        
        # Log the first 200 chars of the email content for debugging
        print(f"[DEBUG] Email content preview: {student_html[:200]}...", flush=True)
        
        # Send the email
        email_sent = send_student_email_via_brevo_api(
            subject=f"Update on Your Ticket #{ticket.ticket_id}: Escalated",
            message=student_html,
            recipient_email=student_email
        )
        
        if email_sent:
            print(f"[SUCCESS] Student notification sent successfully to {student_email}", flush=True)
        else:
            print(f"[WARNING] Failed to send student notification to {student_email}", flush=True)
            
    except Exception as e:
        error_msg = f"[ERROR] Exception while sending to student {student_email}: {str(e)}"
        print(error_msg, flush=True)
        # Continue with other notifications even if student email fails
    # Admin notification template
    admin_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background-color: #FF6B35; color: white; padding: 20px; text-align: center; border-radius: 5px 5px 0 0; }}
            .content {{ padding: 20px; background-color: #f9f9f9; border: 1px solid #ddd; border-radius: 0 0 5px 5px; }}
            .footer {{ text-align: center; margin-top: 20px; font-size: 12px; color: #666; }}
            table.details {{ width: 100%; margin: 20px 0; background: #fff; border-radius: 8px; border: 1px solid #eee; }}
            table.details td {{ padding: 8px 0; }}
        </style>
    </head>
    <body>
        <div class='container'>
            <div class='header'>
                <h1>Ticket Escalation Alert</h1>
            </div>
            <div class='content'>
                <p><strong>IMPORTANT:</strong> A ticket has been escalated to the General department and requires immediate attention.</p>
                <table class='details'>
                    <tr><td><b>Ticket ID:</b></td><td>{ticket.ticket_id}</td></tr>
                    <tr><td><b>Student:</b></td><td>{ticket.student.get_full_name()} ({ticket.student.email})</td></tr>
                    <tr><td><b>Original Department:</b></td><td>{ticket.original_department.name if ticket.original_department else 'N/A'}</td></tr>
                    <tr><td><b>Current Department:</b></td><td>{ticket.department.name}</td></tr>
                    <tr><td><b>Subject:</b></td><td>{ticket.subject}</td></tr>
                    <tr><td><b>Priority:</b></td><td>{ticket.get_priority_display()}</td></tr>
                    <tr><td><b>Escalated By:</b></td><td>{escalated_by.get_full_name() if escalated_by else 'System'}</td></tr>
                    <tr><td><b>Escalated At:</b></td><td>{ticket.escalated_at.strftime('%Y-%m-%d %H:%M:%S') if ticket.escalated_at else 'N/A'}</td></tr>
                    <tr><td><b>Reason:</b></td><td>{reason or 'SLA breach'}</td></tr>
                </table>
                <p>This ticket requires immediate attention from the support team. Please review and take appropriate action.</p>
                <p style='text-align:center;'>
                    <a href='https://apollouniversity.edu.in/admin/tickets/{ticket.ticket_id}' style='display:inline-block; padding:10px 20px; background-color:#FF6B35; color:white; text-decoration:none; border-radius:5px;'>View Ticket in Admin</a>
                </p>
                <p>If you have any questions or need further assistance, please contact the system administrator.</p>
                <p>Best regards,<br>The Support Team<br>Apollo University</p>
            </div>
            <div class='footer'>
                <p>This is an automated message, please do not reply to this email.</p>
                <p>&copy; {datetime.now().year} Apollo University. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Send to original department admin
    if ticket.original_department:
        try:
            original_dept_email = f"{ticket.original_department.name.lower()}@apollouniversity.edu"
            send_student_email_via_brevo_api(
                subject=f"Ticket {ticket.ticket_id} Escalated - Action Required",
                message=admin_html,
                recipient_email=original_dept_email
            )
            print(f"[DEBUG] Escalation notification sent to {original_dept_email}")
        except Exception as e:
            print(f"[ERROR] Failed to send escalation notification to {original_dept_email}: {e}")
    
    # Send to general support team
    try:
        general_support_email = "general.support@apollouniversity.edu"
        send_student_email_via_brevo_api(
            subject=f"New Escalated Ticket {ticket.ticket_id} - Immediate Action Required",
            message=admin_html,
            recipient_email=general_support_email
        )
        print(f"[DEBUG] Escalation notification sent to {general_support_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send escalation notification to {general_support_email}: {e}")
