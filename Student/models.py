from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import uuid
from core.models import Department
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.conf import settings
import os
from datetime import datetime

PRIORITY_CHOICES = [
    ('low', 'Low'),
    ('medium', 'Medium'),
    ('high', 'High'),
    ('urgent', 'Urgent'),
]

STATUS_CHOICES = [
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('on_hold', 'On Hold'),
    ('escalated', 'Escalated'),
    ('resolved', 'Resolved'),
    ('closed', 'Closed'),
]

# For update forms, exclude 'escalated' so users can't set it directly
STATUS_CHOICES_FOR_UPDATE = [
    ('open', 'Open'),
    ('in_progress', 'In Progress'),
    ('on_hold', 'On Hold'),
    ('resolved', 'Resolved'),
    ('closed', 'Closed'),
]

def validate_file_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:  # 5MB
        raise ValidationError("The maximum file size that can be uploaded is 5MB")

class SLAConfig(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    response_time_hours = models.IntegerField(
        default=8,  # Default 8 hours for response
        help_text="Maximum time in hours to first response"
    )
    resolution_time_hours = models.IntegerField(
        default=24,  # Default 24 hours for resolution
        help_text="Maximum time in hours to resolve the ticket"
    )
    escalation_time_hours = models.IntegerField(
        default=24,  # Default 24 hours for escalation
        help_text="Time in hours after which the ticket should be escalated"
    )

    class Meta:
        unique_together = ['department', 'priority']
        verbose_name = "SLA Configuration"
        verbose_name_plural = "SLA Configurations"

    def __str__(self):
        return f"{self.department.name} - {self.get_priority_display()} Priority SLA"

    def save(self, *args, **kwargs):
        if not self.response_time_hours:
            self.response_time_hours = 8
        if not self.resolution_time_hours:
            self.resolution_time_hours = 24
        if not self.escalation_time_hours:
            self.escalation_time_hours = 24
        super().save(*args, **kwargs)

class Ticket(models.Model):
    ticket_id = models.CharField(max_length=20, unique=True, editable=False)
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_tickets')
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    first_response_at = models.DateTimeField(null=True, blank=True)
    sla_breach = models.BooleanField(default=False)
    escalated_at = models.DateTimeField(null=True, blank=True)
    escalated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='escalated_tickets')
    escalation_reason = models.TextField(null=True, blank=True)
    original_department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='original_tickets')
    attachment = models.FileField(
        upload_to='ticket_attachments/',
        null=True,
        blank=True,
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png']
            ),
            validate_file_size
        ]
    )
    
    def save(self, *args, **kwargs):
        if not self.ticket_id:
            year = timezone.now().strftime('%Y')
            dept_code = self.department.name[:3].upper()
            random_id = str(uuid.uuid4()).upper()[:4]
            self.ticket_id = f'AU-{year}-{dept_code}-{random_id}'
        
        if self.status == 'resolved' and not self.resolved_at:
            self.resolved_at = timezone.now()
        elif self.status != 'resolved':
            self.resolved_at = None
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.ticket_id

    @property
    def is_sla_breached(self):
        if self.status in ['resolved', 'closed']:
            return False
        
        sla_config = SLAConfig.objects.get(
            department=self.department,
            priority=self.priority
        )
        
        # Check response time SLA
        if not self.first_response_at:
            time_since_creation = timezone.now() - self.created_at
            if time_since_creation.total_seconds() / 3600 > sla_config.response_time_hours:
                return True
        
        # Check resolution time SLA
        time_since_creation = timezone.now() - self.created_at
        if time_since_creation.total_seconds() / 3600 > sla_config.resolution_time_hours:
            return True
            
        return False

    def should_escalate(self):
        """Check if the ticket should be escalated based on SLA configuration"""
        if self.status in ['resolved', 'closed']:
            return False

        sla_config = SLAConfig.objects.get(
            department=self.department,
            priority=self.priority
        )

        time_since_creation = timezone.now() - self.created_at
        return time_since_creation.total_seconds() / 3600 > sla_config.escalation_time_hours

    def escalate(self, escalated_by, reason=None):
        """
        Escalate the ticket to general category.
        
        Args:
            escalated_by: User who initiated the escalation
            reason: Optional reason for escalation
            
        Returns:
            bool: True if ticket was newly escalated, False if already escalated
            
        Raises:
            Exception: If ticket is already resolved/closed or if escalation fails
        """
        print(f"[DEBUG] ===== ESCALATION STARTED =====", flush=True)
        print(f"[DEBUG] Ticket ID: {self.ticket_id}", flush=True)
        print(f"[DEBUG] Current status: {self.status}", flush=True)
        print(f"[DEBUG] Escalated by: {escalated_by}", flush=True)
        print(f"[DEBUG] Student: {self.student.get_full_name()} ({self.student.email})", flush=True)
        
        # Validate ticket can be escalated
        if self.status in ['resolved', 'closed']:
            error_msg = f"Cannot escalate a ticket that is already {self.status}."
            print(f"[ERROR] {error_msg}", flush=True)
            raise Exception(error_msg)
            
        # If already escalated, just return
        if self.status == 'escalated':
            print(f"[INFO] Ticket {self.ticket_id} is already escalated", flush=True)
            return False
            
        try:
            # Store the original department before changing it
            self.original_department = self.department
            print(f"[DEBUG] Original department: {self.original_department}", flush=True)
            
            # Get or create the General department
            general_dept, created = Department.objects.get_or_create(
                name='General',
                defaults={'sla_hours': 24}  # 24-hour SLA for escalated tickets
            )
            print(f"[DEBUG] {'Created new' if created else 'Found existing'} General department", flush=True)
            
            # Update ticket fields
            self.department = general_dept
            self.status = 'escalated'
            self.escalated_at = timezone.now()
            self.escalated_by = escalated_by
            self.escalation_reason = reason
            
            # Save the ticket
            self.save()
            print(f"[DEBUG] Ticket saved with escalated status", flush=True)
            print(f"[DEBUG] New department: {self.department}", flush=True)
            print(f"[DEBUG] Escalation time: {self.escalated_at}", flush=True)

            # Create ticket update for escalation
            update_comment = f"Ticket escalated to General department. Reason: {reason or 'SLA breach'}"
            print(f"[DEBUG] Creating ticket update: {update_comment}", flush=True)
            TicketUpdate.objects.create(
                ticket=self,
                user=escalated_by,
                comment=update_comment,
                is_internal=True
            )
            
            # Log the escalation in admin
            from django.contrib.admin.models import LogEntry, CHANGE
            from django.contrib.contenttypes.models import ContentType
            print("[DEBUG] Logging escalation to admin...", flush=True)
            LogEntry.objects.create(
                user_id=escalated_by.id,
                content_type_id=ContentType.objects.get_for_model(self).id,
                object_id=self.id,
                object_repr=str(self),
                action_flag=CHANGE,
                change_message=update_comment
            )
            
            # Send notifications to all relevant parties
            self._send_escalation_notifications(escalated_by, reason)
            
            print(f"[DEBUG] Ticket {self.ticket_id} successfully escalated", flush=True)
            return True
            
        except Exception as e:
            error_msg = f"Failed to escalate ticket {self.ticket_id}: {str(e)}"
            print(f"[ERROR] {error_msg}", flush=True)
            raise Exception(error_msg) from e
    
    def _send_escalation_notifications(self, escalated_by, reason=None):
        """
        Send notifications about ticket escalation to relevant parties.
        
        Args:
            escalated_by: User who initiated the escalation
            reason: Optional reason for escalation
        """
        from core.utils import send_escalation_notification_to_admins
        
        print("[DEBUG] Sending escalation notifications...", flush=True)
        try:
            # This will send notifications to:
            # 1. The student who created the ticket
            # 2. Department admins
            # 3. General support team
            send_escalation_notification_to_admins(self, escalated_by, reason)
            print("[DEBUG] Escalation notifications sent successfully", flush=True)
        except Exception as e:
            error_msg = f"Failed to send escalation notifications: {str(e)}"
            print(f"[ERROR] {error_msg}", flush=True)
            # Don't raise the exception here to prevent the escalation from failing
            # just because notifications failed

    def clean(self):
        super().clean()
        if self.attachment:
            # Additional validation can be added here if needed
            pass

    class Meta:
        ordering = ['-created_at']

class TicketUpdate(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='updates')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_internal = models.BooleanField(default=False)  # For internal staff notes

    def __str__(self):
        return f"Update on {self.ticket.ticket_id} by {self.user.username}"

class SLABreachLog(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    breach_type = models.CharField(max_length=20, choices=[
        ('response', 'Response Time'),
        ('resolution', 'Resolution Time'),
    ])
    breached_at = models.DateTimeField(auto_now_add=True)
    notified = models.BooleanField(default=False)

    def __str__(self):
        return f"SLA Breach - {self.ticket.ticket_id} - {self.breach_type}"
