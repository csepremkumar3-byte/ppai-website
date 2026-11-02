from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from submissions.models import UserProfile


class Command(BaseCommand):
    help = "Creates or resets default admin/editor superuser account"

    def handle(self, *args, **options):
        # 1. Primary Chief Editor / Admin requested:
        # Username: editor
        # Password: IJpp@1972
        user, _ = User.objects.get_or_create(username='editor', defaults={'email': 'editor@ppai.org.in'})
        user.email = 'editor@ppai.org.in'
        user.set_password('IJpp@1972')
        user.is_staff = True
        user.is_superuser = True
        user.first_name = 'Chief'
        user.last_name = 'Editor'
        user.save()

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = 'admin'
        profile.is_editor = False
        profile.is_reviewer = False
        profile.is_author = False
        profile.affiliation = 'Plant Protection Association of India (PPAI)'
        profile.save()

        # 2. Also keep 'admin' in sync with the new password
        admin_user = User.objects.filter(username='admin').first()
        if admin_user:
            admin_user.set_password('IJpp@1972')
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.save()
            admin_prof, _ = UserProfile.objects.get_or_create(user=admin_user)
            admin_prof.role = 'admin'
            admin_prof.save()

        self.stdout.write(self.style.SUCCESS(
            "Chief Editor / Admin account ready:\n"
            "  Username : editor (or admin)\n"
            "  Email    : editor@ppai.org.in\n"
            "  Password : IJpp@1972\n"
            "  Role     : Chief Editor / Superuser"
        ))
