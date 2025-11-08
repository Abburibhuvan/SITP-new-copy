from django.core.management.base import BaseCommand
from core.models import Department
from Student.models import Ticket
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = "Clean up duplicate 'General' departments and reassign tickets and users."

    def handle(self, *args, **options):
        with transaction.atomic():
            # Find all departments named 'General' (case-insensitive)
            general_depts = list(Department.objects.filter(name__iexact='General'))
            if not general_depts:
                self.stdout.write(self.style.ERROR("No 'General' department found."))
                return

            # Pick canonical: prefer exact 'General', else first
            canonical = next((d for d in general_depts if d.name == 'General'), general_depts[0])
            duplicates = [d for d in general_depts if d != canonical]

            self.stdout.write(f"Canonical 'General' department: {canonical.id} ({canonical.name})")
            if not duplicates:
                self.stdout.write(self.style.SUCCESS("No duplicate 'General' departments found."))
                return

            # Reassign tickets
            ticket_count = 0
            for dup in duplicates:
                t1 = Ticket.objects.filter(department=dup).update(department=canonical)
                t2 = Ticket.objects.filter(original_department=dup).update(original_department=canonical)
                ticket_count += t1 + t2

            # Reassign user profiles (if applicable)
            from core.models import Profile
            profile_count = 0
            if hasattr(Profile, 'department'):
                for dup in duplicates:
                    profile_count += Profile.objects.filter(department=dup).update(department=canonical)

            # Delete duplicates
            deleted_ids = [d.id for d in duplicates]
            Department.objects.filter(id__in=deleted_ids).delete()

            self.stdout.write(self.style.SUCCESS(
                f"Reassigned {ticket_count} tickets and {profile_count} profiles. Deleted {len(deleted_ids)} duplicate departments."
            )) 