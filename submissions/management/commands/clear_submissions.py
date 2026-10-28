import os
import shutil
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.conf import settings
from submissions.models import UserProfile, Manuscript, ReviewAssignment, ManuscriptRevision, SubmissionActivityLog
from pages.models import NewsletterSubscriber


class Command(BaseCommand):
    help = "Deletes all login, registration, and submission data while preserving society content."

    def add_arguments(self, parser):
        parser.add_argument(
            '--no-admin',
            action='store_true',
            help='Do not recreate the default admin user after wiping.',
        )
        parser.add_argument(
            '--admin-password',
            type=str,
            default='AdminPassword123!',
            help='Password for the restored admin account (default: AdminPassword123!).',
        )

    def handle(self, *args, **options):
        no_admin = options.get('no_admin', False)
        admin_password = options.get('admin_password', 'AdminPassword123!')

        # 1. Clear sessions
        Session.objects.all().delete()

        # 2. Clear editorial & submission data
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

        # 3. Clear newsletter subscribers
        news_count = NewsletterSubscriber.objects.count()
        NewsletterSubscriber.objects.all().delete()

        # 4. Clear all user accounts
        deleted_users, _ = User.objects.all().delete()

        # 5. Clean media folders for manuscripts and payment screenshots
        media_root = getattr(settings, 'MEDIA_ROOT', None)
        cleaned_files = 0
        if media_root and os.path.exists(media_root):
            manuscripts_dir = os.path.join(media_root, 'manuscripts')
            if os.path.exists(manuscripts_dir):
                shutil.rmtree(manuscripts_dir, ignore_errors=True)
                os.makedirs(manuscripts_dir, exist_ok=True)
                cleaned_files += 1

            payments_dir = os.path.join(media_root, 'submissions', 'payments')
            if os.path.exists(payments_dir):
                shutil.rmtree(payments_dir, ignore_errors=True)
                os.makedirs(payments_dir, exist_ok=True)
                cleaned_files += 1

        msg = (
            f"Successfully deleted all login, registration, and submission data:\n"
            f" - {deleted_users} User account(s) deleted\n"
            f" - {prof_count} User profile(s) deleted\n"
            f" - {manu_count} Manuscript submission(s) deleted\n"
            f" - {rev_count} Review assignment(s) deleted\n"
            f" - {rev_sub_count} Manuscript revision(s) deleted\n"
            f" - {act_count} Submission log(s) deleted\n"
            f" - {news_count} Newsletter subscriber(s) deleted\n"
            f" - All user sessions cleared\n"
            f" - Test upload media directories cleared.\n"
        )

        # 6. Recreate clean default Chief Editor / Admin
        if not no_admin:
            # Primary admin user: admin@ppai.org.in
            admin_user = User.objects.create_superuser(
                username='admin@ppai.org.in',
                email='admin@ppai.org.in',
                password=admin_password,
                first_name='Chief',
                last_name='Editor'
            )
            p1, _ = UserProfile.objects.get_or_create(user=admin_user)
            p1.role = 'editor'
            p1.is_editor = True
            p1.is_author = True
            p1.affiliation = 'Plant Protection Association of India (PPAI)'
            p1.save()

            # Username alias: admin
            admin_alias = User.objects.create_superuser(
                username='admin',
                email='admin@ppai.org.in',
                password=admin_password,
                first_name='Chief',
                last_name='Editor'
            )
            p2, _ = UserProfile.objects.get_or_create(user=admin_alias)
            p2.role = 'editor'
            p2.is_editor = True
            p2.is_author = True
            p2.affiliation = 'Plant Protection Association of India (PPAI)'
            p2.save()

            msg += (
                f"\nClean Chief Editor / Admin account restored:\n"
                f"  Username / Email: admin@ppai.org.in (or 'admin')\n"
                f"  Password:         {admin_password}\n"
                f"  Role:             Chief Editor / Superuser"
            )

        self.stdout.write(self.style.SUCCESS(msg))
