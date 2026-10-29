from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from submissions.models import ReviewAssignment
from submissions.emails import send_reviewer_reminder


class Command(BaseCommand):
    help = "Dispatches automated follow-up reminder emails to reviewers with pending invitations."

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=3,
            help='Days elapsed after assignment before sending reminder (default: 3 days).',
        )

    def handle(self, *args, **options):
        days = options.get('days', 3)
        threshold_date = timezone.now() - timedelta(days=days)

        pending_assignments = ReviewAssignment.objects.filter(
            status='pending',
            invitation_date__lte=threshold_date
        )

        sent_count = 0
        for assignment in pending_assignments:
            try:
                send_reviewer_reminder(assignment)
                sent_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"Reminder sent to {assignment.reviewer.email} for manuscript {assignment.manuscript.tracking_id}"
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Failed to send reminder for assignment {assignment.id}: {e}"
                ))

        self.stdout.write(self.style.SUCCESS(
            f"Review reminder run complete: {sent_count} reminder(s) dispatched."
        ))
