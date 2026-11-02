import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import timedelta
from submissions.models import (
    UserProfile,
    Manuscript,
    ReviewAssignment,
    SubmissionActivityLog
)


class Command(BaseCommand):
    help = "Creates verified test profiles and sample workflow manuscripts for testing the PPAI Editorial Portal."

    def add_arguments(self, parser):
        parser.add_argument(
            '--password',
            type=str,
            default='PpaiTest2026!',
            help='Password to set for all test accounts (default: PpaiTest2026!).'
        )
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Reset existing test manuscripts and review assignments before recreating.'
        )

    def handle(self, *args, **options):
        password = options.get('password')
        reset = options.get('reset')

        self.stdout.write(self.style.NOTICE("Initializing PPAI Editorial Portal Test Profiles & Sample Data..."))

        # 1. Clean previous sample manuscripts if requested
        if reset:
            sample_ids = [
                'PPAI-2026-0001', 'PPAI-2026-0002', 'PPAI-2026-0003',
                'PPAI-2026-0004', 'PPAI-2026-0005'
            ]
            deleted, _ = Manuscript.objects.filter(tracking_id__in=sample_ids).delete()
            self.stdout.write(f"Reset {deleted} existing test manuscripts.")

        # Ensure no duplicate admin usernames with same email
        User.objects.filter(username='admin@ppai.org.in').exclude(username='admin').delete()

        # Helper to create/update user
        def get_or_setup_user(username, email, first_name, last_name, role, user_password=None, is_staff=False, is_super=False, affiliation=""):
            pwd = user_password or password
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email}
            )
            user.email = email
            user.first_name = first_name
            user.last_name = last_name
            user.is_staff = is_staff
            user.is_superuser = is_super
            user.set_password(pwd)
            user.save()

            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.role = role
            profile.affiliation = affiliation
            if role == 'admin':
                profile.is_editor = False
                profile.is_reviewer = False
                profile.is_author = False
            elif role == 'editor':
                profile.is_editor = True
                profile.is_approved_editor = True
                profile.is_reviewer = False
                profile.is_author = False
            elif role == 'reviewer':
                profile.is_editor = False
                profile.is_reviewer = True
                profile.is_approved_reviewer = True
                profile.is_author = False
            elif role == 'author':
                profile.is_editor = False
                profile.is_reviewer = False
                profile.is_author = True
            profile.save()
            return user

        # -------------------------------------------------------------
        # 1. Provision Test Accounts
        # -------------------------------------------------------------
        # Chief Editor (Username: editor / Password: IJpp@1972)
        chief_editor = get_or_setup_user(
            username='editor',
            email='editor@ppai.org.in',
            first_name='Dr. Chief',
            last_name='Editor',
            role='admin',
            user_password='IJpp@1972',
            is_staff=True,
            is_super=True,
            affiliation='Plant Protection Association of India (PPAI)'
        )

        # Also configure 'admin' username with IJpp@1972
        get_or_setup_user(
            username='admin',
            email='admin@ppai.org.in',
            first_name='Chief',
            last_name='Editor',
            role='admin',
            user_password='IJpp@1972',
            is_staff=True,
            is_super=True,
            affiliation='Plant Protection Association of India (PPAI)'
        )

        # Associate Editor
        assoc_editor = get_or_setup_user(
            username='associate.editor@ppai.org.in',
            email='associate.editor@ppai.org.in',
            first_name='Dr. Ramesh',
            last_name='Sharma',
            role='editor',
            is_staff=True,
            is_super=False,
            affiliation='ICAR - Indian Agricultural Research Institute (IARI), New Delhi'
        )

        # Reviewer
        reviewer = get_or_setup_user(
            username='reviewer@ppai.org.in',
            email='reviewer@ppai.org.in',
            first_name='Prof. Sunita',
            last_name='Rao',
            role='reviewer',
            is_staff=False,
            is_super=False,
            affiliation='Department of Entomology, Agricultural University, Hyderabad'
        )

        # Author
        author = get_or_setup_user(
            username='author@ppai.org.in',
            email='author@ppai.org.in',
            first_name='Dr. Rajesh',
            last_name='Patel',
            role='author',
            is_staff=False,
            is_super=False,
            affiliation='Department of Plant Pathology, University of Agricultural Sciences'
        )

        # Mock files
        mock_pdf = ContentFile(b"%PDF-1.4 Mock manuscript content for peer review testing.", name="sample_manuscript.pdf")
        mock_receipt = ContentFile(b"Mock payment receipt image bytes.", name="payment_receipt.png")

        # -------------------------------------------------------------
        # 2. Seed Sample Manuscripts Across Key Workflow Stages
        # -------------------------------------------------------------
        now = timezone.now()

        # Manuscript 1: Received / Initial Screening
        m1, _ = Manuscript.objects.update_or_create(
            tracking_id='PPAI-2026-0001',
            defaults={
                'author': author,
                'title': 'Efficacy of Biocontrol Agents against Xanthomonas oryzae in Paddy',
                'abstract': 'Comprehensive field and lab evaluation of bacterial leaf blight biocontrol using antagonistic Pseudomonas strains across varying rice agro-climatic zones.',
                'keywords': 'Xanthomonas, bacterial blight, biocontrol, Pseudomonas, Oryza sativa',
                'article_type': 'research_article',
                'subject_area': 'pathology',
                'status': 'submitted',
                'editor_decision': 'pending',
                'payment_transaction_id': 'UPI/SBI/2026103001',
                'conflict_of_interest': True,
            }
        )
        if not m1.manuscript_file:
            m1.manuscript_file.save("PPAI-2026-0001_manuscript.pdf", mock_pdf, save=False)
        if not m1.payment_screenshot:
            m1.payment_screenshot.save("PPAI-2026-0001_receipt.png", mock_receipt, save=False)
        m1.save()

        # Manuscript 2: Pending Reviewer Invitation
        m2, _ = Manuscript.objects.update_or_create(
            tracking_id='PPAI-2026-0002',
            defaults={
                'author': author,
                'title': 'Nanoparticle Formulations of Trichoderma viride for Root Rot Management',
                'abstract': 'Synthesis and bio-efficacy evaluation of chitosan-functionalized Trichoderma nanoparticles against Macrophomina phaseolina in pulse crops.',
                'keywords': 'Trichoderma, root rot, nanoparticles, Macrophomina, pulse protection',
                'article_type': 'research_article',
                'subject_area': 'biocontrol',
                'status': 'under_review',
                'assigned_editor': assoc_editor,
                'editor_decision': 'pending',
                'payment_transaction_id': 'UPI/HDFC/2026103002',
                'conflict_of_interest': True,
            }
        )
        if not m2.manuscript_file:
            m2.manuscript_file.save("PPAI-2026-0002_manuscript.pdf", mock_pdf, save=False)
        if not m2.payment_screenshot:
            m2.payment_screenshot.save("PPAI-2026-0002_receipt.png", mock_receipt, save=False)
        m2.save()

        # Review Assignment 1 (Pending Invitation)
        r_pending, _ = ReviewAssignment.objects.update_or_create(
            manuscript=m2,
            reviewer=reviewer,
            defaults={
                'assigned_by': chief_editor,
                'status': 'pending',
                'due_date': (now + timedelta(days=21)).date(),
                'reminder_sent': False,
            }
        )

        # Manuscript 3: Review In Progress / Accepted Invitation
        m3, _ = Manuscript.objects.update_or_create(
            tracking_id='PPAI-2026-0003',
            defaults={
                'author': author,
                'title': 'Molecular Characterization of Fall Armyworm Resistance in Maize Ecosystems',
                'abstract': 'Genomic screening of Spodoptera frugiperda populations across southern states to detect cry1Ac and cry2Ab tolerance alleles.',
                'keywords': 'Spodoptera frugiperda, Fall Armyworm, Bt resistance, maize, pest genomics',
                'article_type': 'research_article',
                'subject_area': 'entomology',
                'status': 'under_review',
                'assigned_editor': assoc_editor,
                'editor_decision': 'pending',
                'payment_transaction_id': 'UPI/ICICI/2026103003',
                'conflict_of_interest': True,
            }
        )
        if not m3.manuscript_file:
            m3.manuscript_file.save("PPAI-2026-0003_manuscript.pdf", mock_pdf, save=False)
        if not m3.payment_screenshot:
            m3.payment_screenshot.save("PPAI-2026-0003_receipt.png", mock_receipt, save=False)
        m3.save()

        # Review Assignment 2 (Accepted, Reviewer actively evaluating)
        r_active, _ = ReviewAssignment.objects.update_or_create(
            manuscript=m3,
            reviewer=reviewer,
            defaults={
                'assigned_by': assoc_editor,
                'status': 'accepted',
                'due_date': (now + timedelta(days=14)).date(),
                'reminder_sent': False,
            }
        )

        # Manuscript 4: Sent Back to Author (Revisions Requested)
        m4, _ = Manuscript.objects.update_or_create(
            tracking_id='PPAI-2026-0004',
            defaults={
                'author': author,
                'title': 'Survey of Invasive Whitefly Infestations in Telangana Cotton Belts',
                'abstract': 'Epidemiological survey of Bemisia tabaci biotypes and geminivirus transmission dynamics in high-density cotton farming.',
                'keywords': 'Bemisia tabaci, whitefly, cotton, geminivirus, Telangana epidemiology',
                'article_type': 'research_article',
                'subject_area': 'entomology',
                'status': 'revisions_requested',
                'editor_decision': 'minor_revision',
                'editor_comments_to_author': (
                    "Please address Reviewer 1's feedback regarding sampling intervals: "
                    "1. Clarify whether trap counts were recorded weekly or bi-weekly. "
                    "2. Include ANOVA table in Table 3. "
                    "3. Submit a point-by-point response and revised manuscript."
                ),
                'payment_transaction_id': 'UPI/SBI/2026103004',
                'conflict_of_interest': True,
            }
        )
        if not m4.manuscript_file:
            m4.manuscript_file.save("PPAI-2026-0004_manuscript.pdf", mock_pdf, save=False)
        if not m4.payment_screenshot:
            m4.payment_screenshot.save("PPAI-2026-0004_receipt.png", mock_receipt, save=False)
        m4.save()

        # Manuscript 5: Accepted for Publication
        m5, _ = Manuscript.objects.update_or_create(
            tracking_id='PPAI-2026-0005',
            defaults={
                'author': author,
                'title': 'Genomic Insights into Yellow Vein Mosaic Virus Resistance in Okra Germplasm',
                'abstract': 'Identification of single nucleotide polymorphisms associated with YVMV resistance in wild Abelmoschus species accessions.',
                'keywords': 'Yellow Vein Mosaic Virus, okra, germplasm resistance, Abelmoschus, SNP',
                'article_type': 'research_article',
                'subject_area': 'pathology',
                'status': 'accepted',
                'editor_decision': 'accept',
                'editor_comments_to_author': 'Manuscript has been formally accepted for publication in the upcoming volume of Plant Protection Association of India.',
                'payment_transaction_id': 'UPI/PNB/2026103005',
                'conflict_of_interest': True,
            }
        )
        if not m5.manuscript_file:
            m5.manuscript_file.save("PPAI-2026-0005_manuscript.pdf", mock_pdf, save=False)
        if not m5.payment_screenshot:
            m5.payment_screenshot.save("PPAI-2026-0005_receipt.png", mock_receipt, save=False)
        m5.save()

        # Log Activity
        SubmissionActivityLog.objects.get_or_create(
            manuscript=m1,
            action="Manuscript Received",
            defaults={'user': author, 'details': 'Initial manuscript submission lodged with payment verification.'}
        )
        SubmissionActivityLog.objects.get_or_create(
            manuscript=m2,
            action="Reviewer Invitation Sent",
            defaults={'user': chief_editor, 'details': f"Invitation dispatched to reviewer {reviewer.email}."}
        )
        SubmissionActivityLog.objects.get_or_create(
            manuscript=m3,
            action="Review Invitation Accepted",
            defaults={'user': reviewer, 'details': f"Reviewer {reviewer.email} confirmed peer review commitment."}
        )
        SubmissionActivityLog.objects.get_or_create(
            manuscript=m4,
            action="Revisions Requested",
            defaults={'user': chief_editor, 'details': "Minor revisions requested from author."}
        )
        SubmissionActivityLog.objects.get_or_create(
            manuscript=m5,
            action="Manuscript Accepted",
            defaults={'user': chief_editor, 'details': "Manuscript accepted for publication."}
        )

        # Output Summary
        self.stdout.write(self.style.SUCCESS(
            "\n" + "=" * 70 + "\n"
            " SUCCESS: Test Profiles & Sample Workflow Data Provisioned!\n"
            "=" * 70 + "\n\n"
            "Standard Password for Associate Editor, Reviewer, and Author: " + password + "\n\n"
            "1. CHIEF EDITOR / ADMIN\n"
            "   - Username         : editor (or admin)\n"
            "   - Login (Email)    : editor@ppai.org.in (or admin@ppai.org.in)\n"
            "   - Password         : IJpp@1972\n"
            "   - Role Selected    : Chief Editor\n"
            "   - Target Dashboard : /portal/admin/\n"
            "   - Capabilities     : Workflow stats, assign editors/reviewers, accept/reject/publish\n\n"
            "2. ASSOCIATE EDITOR\n"
            "   - Login (Email)    : associate.editor@ppai.org.in\n"
            "   - Password         : " + password + "\n"
            "   - Role Selected    : Associate Editor\n"
            "   - Target Dashboard : /portal/editor/\n"
            "   - Capabilities     : Review assigned manuscripts, manage reviewers, submit recommendation\n\n"
            "3. REVIEWER\n"
            "   - Login (Email)    : reviewer@ppai.org.in\n"
            "   - Password         : " + password + "\n"
            "   - Role Selected    : Reviewer\n"
            "   - Target Dashboard : /portal/reviewer/\n"
            "   - Capabilities     : Accept/decline invitations, submit review scores & feedback\n\n"
            "4. AUTHOR\n"
            "   - Login (Email)    : author@ppai.org.in\n"
            "   - Password         : " + password + "\n"
            "   - Role Selected    : Author\n"
            "   - Target Dashboard : /portal/author/\n"
            "   - Capabilities     : Submit new manuscript, view status, submit revisions\n\n"
            "----------------------------------------------------------------------\n"
            "Pre-Seeded Sample Manuscripts for Immediate Testing:\n"
            " * PPAI-2026-0001 : [Received] Ready for Chief Editor assignment\n"
            " * PPAI-2026-0002 : [Under Review] Reviewer has pending invitation (Accept/Decline)\n"
            " * PPAI-2026-0003 : [Under Review] Reviewer accepted, ready to evaluate & submit score\n"
            " * PPAI-2026-0004 : [Sent Back to Author] Author can submit revision & responses\n"
            " * PPAI-2026-0005 : [Accepted] Chief Editor can mark as Published\n"
            "=" * 70 + "\n"
        ))
