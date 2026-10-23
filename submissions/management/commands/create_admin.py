from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from submissions.models import UserProfile


class Command(BaseCommand):
    help = "Creates or resets default admin/editor superuser account"

    def handle(self, *args, **options):
        # Create/reset admin@ppai.org.in
        user, _ = User.objects.get_or_create(username='admin@ppai.org.in', defaults={'email': 'admin@ppai.org.in'})
        user.email = 'admin@ppai.org.in'
        user.set_password('AdminPassword123!')
        user.is_staff = True
        user.is_superuser = True
        user.first_name = 'Chief'
        user.last_name = 'Editor'
        user.save()

        profile, _ = UserProfile.objects.get_or_create(user=user)
        profile.role = 'editor'
        profile.is_editor = True
        profile.is_author = True
        profile.affiliation = 'Plant Protection Association of India (PPAI)'
        profile.save()

        # Also create 'admin' alias
        user_alias, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@ppai.org.in'})
        user_alias.email = 'admin@ppai.org.in'
        user_alias.set_password('AdminPassword123!')
        user_alias.is_staff = True
        user_alias.is_superuser = True
        user_alias.save()

        profile_alias, _ = UserProfile.objects.get_or_create(user=user_alias)
        profile_alias.role = 'editor'
        profile_alias.is_editor = True
        profile_alias.is_author = True
        profile_alias.affiliation = 'Plant Protection Association of India (PPAI)'
        profile_alias.save()

        self.stdout.write(self.style.SUCCESS(
            "Admin superuser ready:\n"
            "  Username / Email : admin@ppai.org.in (or admin)\n"
            "  Password         : AdminPassword123!\n"
            "  Role             : Editor / Superuser"
        ))
