from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from submissions.models import UserProfile


class Command(BaseCommand):
    help = "Creates or resets default admin/editor superuser account"

    def handle(self, *args, **options):
        user, _ = User.objects.get_or_create(username='admin', defaults={'email': 'admin@ppai.org.in'})
        user.email = 'admin@ppai.org.in'
        user.set_password('AdminPassword123!')
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

        self.stdout.write(self.style.SUCCESS(
            "Chief Editor admin superuser ready:\n"
            "  Username : admin\n"
            "  Email    : admin@ppai.org.in\n"
            "  Password : AdminPassword123!\n"
            "  Role     : Chief Editor / Superuser"
        ))
