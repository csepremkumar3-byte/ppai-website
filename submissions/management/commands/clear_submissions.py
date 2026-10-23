from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from submissions.models import UserProfile, Manuscript, ReviewAssignment, ManuscriptRevision, SubmissionActivityLog


class Command(BaseCommand):
    help = "Deletes all login, registration, and submission data while preserving society data."

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset-admin',
            action='store_true',
            help='Recreates a single clean default admin superuser (admin / Admin@12345) after wiping.',
        )

    def handle(self, *args, **options):
        reset_admin = options.get('reset_admin', True)

        Session.objects.all().delete()
        rev_count = ReviewAssignment.objects.count()
        ReviewAssignment.objects.all().delete()

        rev_sub_count = ManuscriptRevision.objects.count()
        ManuscriptRevision.objects.all().delete()

        act_count = SubmissionActivityLog.objects.count()
        SubmissionActivityLog.objects.all().delete()

        manu_count = Manuscript.objects.count()
        Manuscript.objects.all().delete()

        prof_count = UserProfile.objects.count()
        UserProfile.objects.all().delete()

        deleted_users, _ = User.objects.all().delete()

        msg = (
            f"Successfully wiped all login and registration data:\n"
            f" - {deleted_users} User account(s) deleted\n"
            f" - {prof_count} User profile(s) deleted\n"
            f" - {manu_count} Manuscript(s) deleted\n"
            f" - {rev_count} Review assignment(s) deleted\n"
            f" - All active sessions cleared.\n"
        )

        if reset_admin:
            admin_user = User.objects.create_superuser('admin', 'admin@ppai.org.in', 'Admin@12345')
            p, _ = UserProfile.objects.get_or_create(user=admin_user)
            p.role = 'editor'
            p.is_editor = True
            p.is_author = True
            p.save()
            msg += "\nClean default admin restored: admin / Admin@12345 (role: Editor)."

        self.stdout.write(self.style.SUCCESS(msg))
