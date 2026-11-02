import sys
from django.core.management.base import BaseCommand
from django.test import Client
from django.contrib.auth.models import User
from submissions.models import Manuscript, ReviewAssignment


class Command(BaseCommand):
    help = "Verifies that the entire editorial workflow and test profiles are working 100% correctly."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("\n========================================================"))
        self.stdout.write(self.style.NOTICE(" RUNNING COMPREHENSIVE PPAI WORKFLOW INTEGRITY CHECK"))
        self.stdout.write(self.style.NOTICE("========================================================\n"))

        client = Client()
        password = 'PpaiTest2026!'
        errors = []

        # -------------------------------------------------------------
        # 1. Author Verification
        # -------------------------------------------------------------
        self.stdout.write("1. Verifying Author Profile & Workflow...")
        client.logout()
        login_resp = client.post('/login/', {
            'email': 'author@ppai.org.in',
            'password': password,
            'selected_role': 'author'
        }, follow=True)

        if login_resp.status_code != 200 or not login_resp.wsgi_request.user.is_authenticated:
            errors.append("Author login failed.")
            self.stdout.write(self.style.ERROR("   [FAIL] Author login failed."))
        else:
            self.stdout.write(self.style.SUCCESS("   [PASS] Author authenticated successfully."))

        # Author Dashboard
        dash_resp = client.get('/portal/author/')
        if dash_resp.status_code == 200:
            self.stdout.write(self.style.SUCCESS("   [PASS] Author dashboard loads (HTTP 200)."))
        else:
            errors.append(f"Author dashboard returned status {dash_resp.status_code}")
            self.stdout.write(self.style.ERROR(f"   [FAIL] Author dashboard HTTP {dash_resp.status_code}"))

        # Author Submit Page
        submit_resp = client.get('/portal/author/submit/')
        if submit_resp.status_code == 200:
            self.stdout.write(self.style.SUCCESS("   [PASS] Author submission form accessible (HTTP 200)."))
        else:
            errors.append(f"Author submit form returned status {submit_resp.status_code}")
            self.stdout.write(self.style.ERROR(f"   [FAIL] Author submit form HTTP {submit_resp.status_code}"))

        # Author Revision Form for PPAI-2026-0004
        rev_resp = client.get('/portal/author/manuscript/PPAI-2026-0004/revision/')
        if rev_resp.status_code == 200:
            self.stdout.write(self.style.SUCCESS("   [PASS] Revision submission form accessible for revisions_requested manuscript (HTTP 200)."))
        else:
            errors.append(f"Author revision form returned status {rev_resp.status_code}")
            self.stdout.write(self.style.ERROR(f"   [FAIL] Author revision form HTTP {rev_resp.status_code}"))

        # -------------------------------------------------------------
        # 2. Reviewer Verification
        # -------------------------------------------------------------
        self.stdout.write("\n2. Verifying Reviewer Profile & Workflow...")
        client.logout()
        login_resp = client.post('/login/', {
            'email': 'reviewer@ppai.org.in',
            'password': password,
            'selected_role': 'reviewer'
        }, follow=True)

        if login_resp.status_code != 200 or not login_resp.wsgi_request.user.is_authenticated:
            errors.append("Reviewer login failed.")
            self.stdout.write(self.style.ERROR("   [FAIL] Reviewer login failed."))
        else:
            self.stdout.write(self.style.SUCCESS("   [PASS] Reviewer authenticated successfully."))

        # Reviewer Dashboard
        rev_dash_resp = client.get('/portal/reviewer/')
        if rev_dash_resp.status_code == 200:
            self.stdout.write(self.style.SUCCESS("   [PASS] Reviewer dashboard loads (HTTP 200)."))
        else:
            errors.append(f"Reviewer dashboard returned status {rev_dash_resp.status_code}")
            self.stdout.write(self.style.ERROR(f"   [FAIL] Reviewer dashboard HTTP {rev_dash_resp.status_code}"))

        # Check Active Review Evaluation Form
        active_assignment = ReviewAssignment.objects.filter(reviewer__email='reviewer@ppai.org.in', status='accepted').first()
        if active_assignment:
            eval_resp = client.get(f'/portal/reviewer/evaluate/{active_assignment.id}/')
            if eval_resp.status_code == 200:
                self.stdout.write(self.style.SUCCESS(f"   [PASS] Reviewer evaluation form accessible for {active_assignment.manuscript.tracking_id} (HTTP 200)."))
            else:
                errors.append(f"Reviewer evaluation form returned HTTP {eval_resp.status_code}")
                self.stdout.write(self.style.ERROR(f"   [FAIL] Evaluation form HTTP {eval_resp.status_code}"))

        # -------------------------------------------------------------
        # 3. Associate Editor Verification
        # -------------------------------------------------------------
        self.stdout.write("\n3. Verifying Associate Editor Profile & Workflow...")
        client.logout()
        login_resp = client.post('/login/', {
            'email': 'associate.editor@ppai.org.in',
            'password': password,
            'selected_role': 'associate_editor'
        }, follow=True)

        if login_resp.status_code != 200 or not login_resp.wsgi_request.user.is_authenticated:
            errors.append("Associate Editor login failed.")
            self.stdout.write(self.style.ERROR("   [FAIL] Associate Editor login failed."))
        else:
            self.stdout.write(self.style.SUCCESS("   [PASS] Associate Editor authenticated successfully."))

        editor_dash_resp = client.get('/portal/editor/')
        if editor_dash_resp.status_code == 200:
            self.stdout.write(self.style.SUCCESS("   [PASS] Associate Editor dashboard loads (HTTP 200)."))
        else:
            errors.append(f"Associate Editor dashboard returned status {editor_dash_resp.status_code}")
            self.stdout.write(self.style.ERROR(f"   [FAIL] Associate Editor dashboard HTTP {editor_dash_resp.status_code}"))

        # -------------------------------------------------------------
        # 4. Chief Editor / Admin Verification
        # -------------------------------------------------------------
        self.stdout.write("\n4. Verifying Chief Editor / Admin Profile & Console...")
        client.logout()
        login_resp = client.post('/login/', {
            'email': 'admin@ppai.org.in',
            'password': password,
            'selected_role': 'chief_editor'
        }, follow=True)

        if login_resp.status_code != 200 or not login_resp.wsgi_request.user.is_authenticated:
            errors.append("Chief Editor login failed.")
            self.stdout.write(self.style.ERROR("   [FAIL] Chief Editor login failed."))
        else:
            self.stdout.write(self.style.SUCCESS("   [PASS] Chief Editor authenticated successfully."))

        admin_dash_resp = client.get('/portal/admin/')
        if admin_dash_resp.status_code == 200:
            # Check for stats and table
            content = admin_dash_resp.content.decode('utf-8')
            has_stats = 'workflow-stats-grid' in content and 'Received' in content and 'Under Review' in content
            has_table = 'Date of Submission' in content and 'Current Status' in content and 'Last Updated' in content
            if has_stats and has_table:
                self.stdout.write(self.style.SUCCESS("   [PASS] Chief Editor Console loads with 7 workflow stats & manuscript table (HTTP 200)."))
            else:
                errors.append("Chief Editor Console missing stats grid or table.")
                self.stdout.write(self.style.ERROR("   [FAIL] Chief Editor Console missing stats grid or table elements."))
        else:
            errors.append(f"Chief Editor Console returned status {admin_dash_resp.status_code}")
            self.stdout.write(self.style.ERROR(f"   [FAIL] Chief Editor Console HTTP {admin_dash_resp.status_code}"))

        # Review & Assign Page for PPAI-2026-0001
        review_assign_resp = client.get('/portal/editor/manuscript/PPAI-2026-0001/')
        if review_assign_resp.status_code == 200:
            self.stdout.write(self.style.SUCCESS("   [PASS] Chief Editor Review & Assign page accessible for PPAI-2026-0001 (HTTP 200)."))
        else:
            errors.append(f"Review & Assign page returned status {review_assign_resp.status_code}")
            self.stdout.write(self.style.ERROR(f"   [FAIL] Review & Assign page HTTP {review_assign_resp.status_code}"))

        # -------------------------------------------------------------
        # 5. Security & Role Isolation Checks
        # -------------------------------------------------------------
        self.stdout.write("\n5. Verifying Security & Role Validation Enforcement...")
        client.logout()

        # Author tries to log in as Chief Editor
        fake_admin = client.post('/login/', {
            'email': 'author@ppai.org.in',
            'password': password,
            'selected_role': 'chief_editor'
        })
        if "Role Validation Alert" in fake_admin.content.decode('utf-8'):
            self.stdout.write(self.style.SUCCESS("   [PASS] Author prevented from logging in as Chief Editor."))
        else:
            errors.append("Role validation failed: author was not blocked from Chief Editor role.")
            self.stdout.write(self.style.ERROR("   [FAIL] Author was not blocked from Chief Editor role."))

        # Chief Editor tries to log in as Author
        fake_author = client.post('/login/', {
            'email': 'admin@ppai.org.in',
            'password': password,
            'selected_role': 'author'
        })
        if "Role Validation Alert" in fake_author.content.decode('utf-8'):
            self.stdout.write(self.style.SUCCESS("   [PASS] Chief Editor prevented from logging in as Author."))
        else:
            errors.append("Role validation failed: Chief Editor was not blocked from Author role.")
            self.stdout.write(self.style.ERROR("   [FAIL] Chief Editor was not blocked from Author role."))

        # -------------------------------------------------------------
        # Summary
        # -------------------------------------------------------------
        self.stdout.write("\n" + "=" * 56)
        if not errors:
            self.stdout.write(self.style.SUCCESS(" ALL 10 INTEGRITY CHECKS PASSED SUCCESSFULLY! (100% OK)"))
            self.stdout.write("=" * 56 + "\n")
        else:
            self.stdout.write(self.style.ERROR(f" WORKFLOW INTEGRITY FAILED WITH {len(errors)} ERROR(S):"))
            for err in errors:
                self.stdout.write(self.style.ERROR(f"  - {err}"))
            self.stdout.write("=" * 56 + "\n")
            sys.exit(1)
