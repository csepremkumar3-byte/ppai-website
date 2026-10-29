import os
from django.test import TestCase, Client, override_settings
from django.core import mail
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from submissions.models import UserProfile, Manuscript, ReviewAssignment, ManuscriptRevision, SubmissionActivityLog
from submissions.emails import (
    send_author_submission_acknowledgment,
    send_chief_editor_submission_alert,
    send_reviewer_invitation,
    send_reviewer_reminder,
    send_chief_editor_reviewer_response,
    send_reviewer_acceptance_confirmation,
    send_user_credentials_email,
    send_chief_editor_review_completed,
    send_author_editorial_decision,
)


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='PPAI Editorial Office <editor@ppai.org.in>',
    CHIEF_EDITOR_EMAIL='editor@ppai.org.in'
)
class EmailWorkflowVerificationTests(TestCase):
    def setUp(self):
        mail.outbox.clear()

        # 1. Chief Editor / Superuser
        self.chief_editor = User.objects.create_superuser(
            username='chief.editor@ppai.org.in',
            email='chief.editor@ppai.org.in',
            password='EditorPass123!',
            first_name='Chief',
            last_name='Editor'
        )
        self.chief_profile = UserProfile.objects.create(
            user=self.chief_editor,
            role='admin',
            is_editor=True,
            is_approved_editor=True,
            affiliation='PPAI Editorial Headquarters'
        )

        # 2. Author
        self.author = User.objects.create_user(
            username='author.researcher@icar.gov.in',
            email='author.researcher@icar.gov.in',
            password='AuthorPass123!',
            first_name='Dr. Ramesh',
            last_name='Verma'
        )
        self.author_profile = UserProfile.objects.create(
            user=self.author,
            role='author',
            is_author=True,
            affiliation='ICAR-IARI Division of Plant Pathology'
        )

        # 3. Reviewer
        self.reviewer = User.objects.create_user(
            username='reviewer.expert@university.edu',
            email='reviewer.expert@university.edu',
            password='ReviewerPass123!',
            first_name='Prof. Priya',
            last_name='Nair'
        )
        self.reviewer_profile = UserProfile.objects.create(
            user=self.reviewer,
            role='reviewer',
            is_reviewer=True,
            is_approved_reviewer=True,
            affiliation='Department of Entomology, Agricultural University'
        )

        # Dummy files
        self.dummy_doc = SimpleUploadedFile("research_paper.pdf", b"%PDF-1.4 Mock manuscript content", content_type="application/pdf")
        self.dummy_proof = SimpleUploadedFile("payment_receipt.png", b"Mock image bytes", content_type="image/png")

    def test_stage_1_submission_emails(self):
        """Verify Email 1 (Author Acknowledgment) and Email 2 (Chief Editor Alert with attachment)."""
        manuscript = Manuscript.objects.create(
            author=self.author,
            title="Genomic Profiling of Xanthomonas oryzae in Rice",
            abstract="Comprehensive study of bacterial blight resistance markers in sub-tropical indica rice varieties.",
            keywords="Xanthomonas, bacterial blight, genomics",
            subject_area="pathology",
            article_type="research_article",
            manuscript_file=self.dummy_doc,
            payment_transaction_id="UPI/9876543210/SBI",
            payment_screenshot=self.dummy_proof,
            conflict_of_interest=True
        )

        # Trigger Email 1: Author Acknowledgment
        send_author_submission_acknowledgment(manuscript)
        self.assertEqual(len(mail.outbox), 1)
        author_mail = mail.outbox[0]
        self.assertIn("author.researcher@icar.gov.in", author_mail.to)
        self.assertIn("Submission Acknowledgment", author_mail.subject)
        self.assertIn(manuscript.tracking_id, author_mail.subject)
        self.assertIn("UPI/9876543210/SBI", author_mail.body)
        self.assertIn("Genomic Profiling of Xanthomonas", author_mail.body)

        # Trigger Email 2: Chief Editor Submission Alert (with manuscript file)
        send_chief_editor_submission_alert(manuscript)
        self.assertEqual(len(mail.outbox), 2)
        editor_mail = mail.outbox[1]
        self.assertIn("editor@ppai.org.in", editor_mail.to)
        self.assertIn("New Submission", editor_mail.subject)
        self.assertIn(manuscript.tracking_id, editor_mail.subject)
        self.assertIn("UPI/9876543210/SBI", editor_mail.body)
        self.assertIn("ICAR-IARI Division of Plant Pathology", editor_mail.body)
        # Check manuscript file is attached
        self.assertEqual(len(editor_mail.attachments), 1)
        self.assertTrue(editor_mail.attachments[0][0].endswith("research_paper.pdf"))

    def test_stage_3_reviewer_invitation_email(self):
        """Verify Email 3 (Reviewer Invitation with window time and interactive Accept/Decline links)."""
        manuscript = Manuscript.objects.create(
            author=self.author,
            title="Biocontrol of Fall Armyworm using Metarhizium anisopliae",
            abstract="Field efficacy trial of entomopathogenic fungus against Spodoptera frugiperda.",
            subject_area="entomology",
            manuscript_file=self.dummy_doc,
            conflict_of_interest=True
        )
        assignment = ReviewAssignment.objects.create(
            manuscript=manuscript,
            reviewer=self.reviewer,
            assigned_by=self.chief_editor
        )

        send_reviewer_invitation(assignment)
        self.assertEqual(len(mail.outbox), 1)
        rev_mail = mail.outbox[0]
        self.assertIn("reviewer.expert@university.edu", rev_mail.to)
        self.assertIn("Review Invitation", rev_mail.subject)
        self.assertIn(manuscript.tracking_id, rev_mail.subject)
        self.assertIn(f"/portal/reviewer/invitation/{assignment.id}/accept/", rev_mail.body)
        self.assertIn(f"/portal/reviewer/invitation/{assignment.id}/decline/", rev_mail.body)
        self.assertIn("Evaluation Window Due Date", rev_mail.body)

    def test_stage_3b_reviewer_response_emails(self):
        """Verify Reviewer Accept/Decline sends confirmation alerts to Chief Editor and Reviewer."""
        manuscript = Manuscript.objects.create(
            author=self.author,
            title="Biocontrol of Fall Armyworm using Metarhizium anisopliae",
            abstract="Field efficacy trial of entomopathogenic fungus against Spodoptera frugiperda.",
            subject_area="entomology",
            manuscript_file=self.dummy_doc,
            conflict_of_interest=True
        )
        assignment = ReviewAssignment.objects.create(
            manuscript=manuscript,
            reviewer=self.reviewer,
            assigned_by=self.chief_editor
        )

        # 1. Reviewer accepts -> Editor gets notification alert
        mail.outbox.clear()
        send_chief_editor_reviewer_response(assignment, action='accepted')
        self.assertEqual(len(mail.outbox), 1)
        editor_alert = mail.outbox[0]
        self.assertIn("editor@ppai.org.in", editor_alert.to)
        self.assertIn("Review Accepted", editor_alert.subject)
        self.assertIn(manuscript.tracking_id, editor_alert.subject)
        self.assertIn(self.reviewer.get_full_name(), editor_alert.body)

        # 2. Reviewer gets confirmation receipt
        mail.outbox.clear()
        send_reviewer_acceptance_confirmation(assignment)
        self.assertEqual(len(mail.outbox), 1)
        rev_conf = mail.outbox[0]
        self.assertIn(self.reviewer.email, rev_conf.to)
        self.assertIn("Peer Review Commitment Confirmed", rev_conf.subject)
        self.assertIn(manuscript.tracking_id, rev_conf.subject)

        # 3. Reviewer declines -> Editor gets reassign alert
        mail.outbox.clear()
        send_chief_editor_reviewer_response(assignment, action='declined')
        self.assertEqual(len(mail.outbox), 1)
        decline_alert = mail.outbox[0]
        self.assertIn("editor@ppai.org.in", decline_alert.to)
        self.assertIn("Review Declined", decline_alert.subject)
        self.assertIn(manuscript.tracking_id, decline_alert.subject)

    def test_stage_3c_reviewer_accept_view_triggers_email_to_editor(self):
        """Verify hitting the accept action view triggers emails to both Editor and Reviewer."""
        manuscript = Manuscript.objects.create(
            author=self.author,
            title="Biocontrol of Fall Armyworm using Metarhizium anisopliae",
            abstract="Field efficacy trial of entomopathogenic fungus against Spodoptera frugiperda.",
            subject_area="entomology",
            manuscript_file=self.dummy_doc,
            conflict_of_interest=True
        )
        assignment = ReviewAssignment.objects.create(
            manuscript=manuscript,
            reviewer=self.reviewer,
            assigned_by=self.chief_editor,
            status='pending'
        )

        mail.outbox.clear()
        self.client.login(username=self.reviewer.username, password='ReviewerPass123!')
        response = self.client.get(
            reverse('reviewer_respond_invitation', kwargs={'assignment_id': assignment.id, 'response_action': 'accept'}),
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        assignment.refresh_from_db()
        self.assertEqual(assignment.status, 'accepted')

        # Check both emails were dispatched: 1 to editor, 1 to reviewer
        self.assertEqual(len(mail.outbox), 2)
        recipients = [m.to[0] for m in mail.outbox]
        self.assertIn('editor@ppai.org.in', recipients)
        self.assertIn(self.reviewer.email, recipients)

    def test_stage_3d_signed_token_one_click_accept_from_email(self):
        """Verify reviewer clicking signed link in email accepts review without prior active session."""
        from django.core.signing import TimestampSigner
        manuscript = Manuscript.objects.create(
            author=self.author,
            title="Biocontrol of Fall Armyworm using Metarhizium anisopliae",
            abstract="Field efficacy trial of entomopathogenic fungus against Spodoptera frugiperda.",
            subject_area="entomology",
            manuscript_file=self.dummy_doc,
            conflict_of_interest=True
        )
        assignment = ReviewAssignment.objects.create(
            manuscript=manuscript,
            reviewer=self.reviewer,
            assigned_by=self.chief_editor,
            status='pending'
        )

        signer = TimestampSigner()
        token = signer.sign(f"{assignment.id}:{assignment.reviewer_id}")

        mail.outbox.clear()
        # Unauthenticated client simulates opening link from external email client
        anon_client = Client()
        response = anon_client.get(
            f"{reverse('reviewer_respond_invitation', kwargs={'assignment_id': assignment.id, 'response_action': 'accept'})}?token={token}",
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        assignment.refresh_from_db()
        self.assertEqual(assignment.status, 'accepted')

        # Check editor got the notification and reviewer got confirmation
        self.assertEqual(len(mail.outbox), 2)
        recipients = [m.to[0] for m in mail.outbox]
        self.assertIn('editor@ppai.org.in', recipients)
        self.assertIn(self.reviewer.email, recipients)

    def test_stage_3e_reviewer_reminder_email(self):
        """Verify Trigger 3 Reminder sends follow-up reminder with accept/decline links."""
        manuscript = Manuscript.objects.create(
            author=self.author,
            title="Biocontrol of Fall Armyworm using Metarhizium anisopliae",
            abstract="Field efficacy trial of entomopathogenic fungus against Spodoptera frugiperda.",
            subject_area="entomology",
            manuscript_file=self.dummy_doc,
            conflict_of_interest=True
        )
        assignment = ReviewAssignment.objects.create(
            manuscript=manuscript,
            reviewer=self.reviewer,
            assigned_by=self.chief_editor,
            status='pending'
        )

        mail.outbox.clear()
        send_reviewer_reminder(assignment)
        self.assertEqual(len(mail.outbox), 1)
        rem_mail = mail.outbox[0]
        self.assertIn(self.reviewer.email, rem_mail.to)
        self.assertIn("Review Reminder", rem_mail.subject)
        self.assertIn(manuscript.tracking_id, rem_mail.subject)
        self.assertIn("Accept URL:", rem_mail.body)
        self.assertIn("Decline URL:", rem_mail.body)

    def test_stage_4_credentials_email(self):
        """Verify Email 4 (Login details dispatched for Reviewer or Associate Editor)."""
        send_user_credentials_email(self.reviewer, "TemporaryPass123!", "Reviewer")
        self.assertEqual(len(mail.outbox), 1)
        cred_mail = mail.outbox[0]
        self.assertIn("reviewer.expert@university.edu", cred_mail.to)
        self.assertIn("Your Reviewer Login Credentials", cred_mail.subject)
        self.assertIn("reviewer.expert@university.edu", cred_mail.body)
        self.assertIn("TemporaryPass123!", cred_mail.body)
        self.assertIn("https://ppai.org.in/login/", cred_mail.body)

    def test_stage_5_review_completed_alert(self):
        """Verify Email 5 (Alert to Chief Editor when review is lodged)."""
        manuscript = Manuscript.objects.create(
            author=self.author,
            title="Studies on Wilt Disease Complex in Chickpea",
            abstract="Fusarium oxysporum f. sp. ciceris interaction study.",
            subject_area="pathology",
            manuscript_file=self.dummy_doc
        )
        assignment = ReviewAssignment.objects.create(
            manuscript=manuscript,
            reviewer=self.reviewer,
            assigned_by=self.chief_editor,
            recommendation='minor_revision',
            status='completed',
            comments_for_author='Well written manuscript. Clarify sample size in table 2.',
            confidential_comments_to_editor='High quality scientific work. Recommend acceptance after minor revisions.'
        )

        send_chief_editor_review_completed(assignment)
        self.assertEqual(len(mail.outbox), 1)
        done_mail = mail.outbox[0]
        self.assertIn("editor@ppai.org.in", done_mail.to)
        self.assertIn("Review Complete", done_mail.subject)
        self.assertIn(manuscript.tracking_id, done_mail.subject)
        self.assertIn("Minor Revision", done_mail.body)

    def test_stage_6_editorial_decision_email(self):
        """Verify Email 6 (Formal Decision Letter + Moderated Peer Comments to Author)."""
        manuscript = Manuscript.objects.create(
            author=self.author,
            title="Studies on Wilt Disease Complex in Chickpea",
            abstract="Fusarium oxysporum f. sp. ciceris interaction study.",
            subject_area="pathology",
            manuscript_file=self.dummy_doc,
            editor_decision='minor_revision',
            editor_comments_to_author='Please address reviewer feedback within 14 days.'
        )
        ReviewAssignment.objects.create(
            manuscript=manuscript,
            reviewer=self.reviewer,
            assigned_by=self.chief_editor,
            recommendation='minor_revision',
            status='completed',
            is_approved_by_editor=True,
            comments_for_author='Minor revision: Expand on inoculation protocol in section 2.3.'
        )

        send_author_editorial_decision(manuscript)
        self.assertEqual(len(mail.outbox), 1)
        dec_mail = mail.outbox[0]
        self.assertIn("author.researcher@icar.gov.in", dec_mail.to)
        self.assertIn("Editorial Decision", dec_mail.subject)
        self.assertIn(manuscript.tracking_id, dec_mail.subject)
        self.assertIn("Minor Revision", dec_mail.body)
        self.assertIn("Expand on inoculation protocol in section 2.3", dec_mail.body)
        self.assertIn("Please address reviewer feedback within 14 days", dec_mail.body)
