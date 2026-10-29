from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from submissions.models import ReviewAssignment, SubmissionActivityLog
from submissions.emails import send_reviewer_reminder, send_chief_editor_invitation_expired


class Command(BaseCommand):
    help = "Dispatches 7-day review reminder emails and marks 14-day expired invitations for Chief Editor reassignment."

    def add_arguments(self, parser):
        parser.add_argument(
            '--reminder-days',
            type=int,
            default=7,
            help='Days elapsed before sending follow-up reminder (default: 7 days).',
        )
        parser.add_argument(
            '--expire-days',
            type=int,
            default=14,
            help='Days elapsed before marking invitation expired (default: 14 days).',
        )

    def handle(self, *args, **options):
        now = timezone.now()
        reminder_days = options.get('reminder_days', 7)
        expire_days = options.get('expire_days', 14)

        reminder_threshold = now - timedelta(days=reminder_days)
        expire_threshold = now - timedelta(days=expire_days)

        # 1. 14-Day Expiration
        expired_qs = ReviewAssignment.objects.filter(
            status='pending',
            invitation_date__lte=expire_threshold
        )
        expired_count = 0
        for assignment in expired_qs:
            try:
                assignment.status = 'expired'
                assignment.save()
                SubmissionActivityLog.objects.create(
                    manuscript=assignment.manuscript,
                    user=assignment.reviewer,
                    action="Invitation Expired",
                    details=f"Reviewer invitation to {assignment.reviewer.get_full_name() or assignment.reviewer.username} expired after {expire_days} days. Alternate reviewer assignment required."
                )
                send_chief_editor_invitation_expired(assignment)
                expired_count += 1
                self.stdout.write(self.style.WARNING(
                    f"Invitation expired for reviewer {assignment.reviewer.email} on {assignment.manuscript.tracking_id}."
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error marking assignment {assignment.id} expired: {e}"
                ))

        # 2. 7-Day Follow-up Reminder
        remind_qs = ReviewAssignment.objects.filter(
            status='pending',
            invitation_date__lte=reminder_threshold,
            invitation_date__gt=expire_threshold,
            reminder_sent=False
        )
        remind_count = 0
        for assignment in remind_qs:
            try:
                send_reviewer_reminder(assignment)
                assignment.reminder_sent = True
                assignment.reminder_date = now
                assignment.save()
                SubmissionActivityLog.objects.create(
                    manuscript=assignment.manuscript,
                    user=assignment.reviewer,
                    action="Review Reminder Sent",
                    details=f"Automated {reminder_days}-day reminder sent to reviewer {assignment.reviewer.get_full_name() or assignment.reviewer.username}."
                )
                remind_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f"7-day reminder sent to {assignment.reviewer.email} for manuscript {assignment.manuscript.tracking_id}."
                ))
            except Exception as e:
                self.stdout.write(self.style.ERROR(
                    f"Error sending reminder for assignment {assignment.id}: {e}"
                ))

        self.stdout.write(self.style.SUCCESS(
            f"Review deadline run complete: {remind_count} reminder(s) dispatched, {expired_count} invitation(s) marked expired."
        ))
