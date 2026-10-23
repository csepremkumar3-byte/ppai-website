from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from submissions.models import UserProfile, Manuscript, ReviewAssignment, ManuscriptRevision, SubmissionActivityLog


class Command(BaseCommand):
    help = "Deletes all test users, user profiles, manuscripts, and peer review data while keeping society records intact."

    def add_arguments(self, parser):
        parser.add_argument(
            '--keep-superusers',
            action='store_true',
            help='Preserve superuser accounts while deleting all other users and submissions.',
        )

    def handle(self, *args, **options):
        keep_superusers = options.get('keep_superusers', False)

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

        if keep_superusers:
            deleted_users, _ = User.objects.filter(is_superuser=False).delete()
        else:
            deleted_users, _ = User.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(
            f"Successfully cleared:\n"
            f" - {deleted_users} User account(s)\n"
            f" - {prof_count} User profile(s)\n"
            f" - {manu_count} Manuscript(s)\n"
            f" - {rev_count} Review assignment(s)\n"
            f" - {rev_sub_count} Manuscript revision(s)\n"
            f" - {act_count} Submission log(s)\n"
            f"All society data (Executive Council, Editorial Board, Volumes, Awards) remain 100% intact."
        ))
