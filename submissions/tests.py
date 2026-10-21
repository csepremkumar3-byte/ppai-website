import io
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile, Manuscript, ReviewAssignment, ManuscriptRevision, SubmissionActivityLog


class PeerReviewWorkflowTests(TestCase):
    def setUp(self):
        self.client = Client()

        # 1. Setup Editor
        self.editor_user = User.objects.create_user(
            username='editor@ppai.org.in',
            email='editor@ppai.org.in',
            password='EditorPass123!',
            first_name='Chief',
            last_name='Editor'
        )
        self.editor_profile = UserProfile.objects.create(
            user=self.editor_user,
            role='editor',
            is_editor=True,
            is_approved_editor=True,
            affiliation='IJPP Editorial Office'
        )

        # 2. Setup Reviewer
        self.reviewer_user = User.objects.create_user(
            username='reviewer@icar.gov.in',
            email='reviewer@icar.gov.in',
            password='ReviewerPass123!',
            first_name='Dr. Sunita',
            last_name='Rao'
        )
        self.reviewer_profile = UserProfile.objects.create(
            user=self.reviewer_user,
            role='reviewer',
            is_reviewer=True,
            is_approved_reviewer=True,
            affiliation='ICAR-IARI, Division of Entomology',
            specialization='Agricultural Entomology & Biocontrol'
        )

        # 3. Setup Author
        self.author_user = User.objects.create_user(
            username='author@university.edu',
            email='author@university.edu',
            password='AuthorPass123!',
            first_name='Rajesh',
            last_name='Sharma'
        )
        self.author_profile = UserProfile.objects.create(
            user=self.author_user,
            role='author',
            is_author=True,
            affiliation='Department of Plant Pathology, UAS Dharwad'
        )

    def test_01_existing_login_and_role_based_access(self):
        """Test role-based access redirection using existing /login/ endpoint."""
        # Author login -> author_dashboard
        response = self.client.post(reverse('login'), {
            'email': 'author@university.edu',
            'password': 'AuthorPass123!'
        }, follow=True)
        self.assertRedirects(response, reverse('author_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Plant Protection Association of India')
        self.assertContains(response, 'Author manuscript submission')
        self.client.logout()

        # Reviewer login -> reviewer_dashboard
        response = self.client.post(reverse('login'), {
            'email': 'reviewer@icar.gov.in',
            'password': 'ReviewerPass123!'
        }, follow=True)
        self.assertRedirects(response, reverse('reviewer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reviewer (view and edit access)')
        self.client.logout()

        # Editor login -> editor_dashboard
        response = self.client.post(reverse('login'), {
            'email': 'editor@ppai.org.in',
            'password': 'EditorPass123!'
        }, follow=True)
        self.assertRedirects(response, reverse('editor_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editor (view and edit) then approve access')
        self.client.logout()

    def test_02_existing_register_with_roles(self):
        """Test registering Author, Reviewer and Editor via existing /register/ endpoint."""
        # 1. Register new Author
        resp_author = self.client.post(reverse('register'), {
            'full_name': 'Dr. Arun Kumar',
            'email': 'arun.author@icar.gov.in',
            'contact': '+91 9988776655',
            'role': 'author',
            'affiliation': 'ICAR-IIHR Bangalore',
            'designation': 'Senior Scientist',
            'specialization': 'Crop Protection',
            'password': 'SecretPass123!',
            'confirm_password': 'SecretPass123!'
        }, follow=True)
        self.assertRedirects(resp_author, reverse('author_dashboard'))
        self.assertTrue(User.objects.filter(email='arun.author@icar.gov.in').exists())
        self.client.logout()

        # 2. Register new Reviewer
        resp_reviewer = self.client.post(reverse('register'), {
            'full_name': 'Prof. V. Raman',
            'email': 'raman.reviewer@university.ac.in',
            'contact': '+91 9123456789',
            'role': 'reviewer',
            'affiliation': 'TNAU Coimbatore',
            'designation': 'Professor',
            'specialization': 'Insect Virology',
            'password': 'SecretPass123!',
            'confirm_password': 'SecretPass123!'
        }, follow=True)
        self.assertRedirects(resp_reviewer, reverse('reviewer_dashboard'))
        self.assertTrue(User.objects.filter(email='raman.reviewer@university.ac.in').exists())
        self.client.logout()

    def test_03_full_paper_flow_loop(self):
        """End-to-End Paper Flow:
        Register -> Login -> Author manuscript submission -> Editor (view and edit) then approve access ->
        Reviewer (view and edit access) -> Comment on submitted manuscript by author -> Return comments to Authors -> Revision -> Acceptance
        """
        # 1. Author submits manuscript
        dummy_file = SimpleUploadedFile("paper.docx", b"Manuscript content", content_type="application/msword")
        manuscript = Manuscript.objects.create(
            author=self.author_user,
            title="Bio-efficacy of Trichoderma harzianum on Rhizoctonia solani",
            abstract="Study on biological control of sheath blight in paddy crops.",
            keywords="Trichoderma, Rhizoctonia, rice sheath blight",
            article_type="research_article",
            subject_area="pathology",
            manuscript_file=dummy_file,
            conflict_of_interest=True
        )
        self.assertTrue(manuscript.tracking_id.startswith('IJPP-'))

        # 2. Editor views paper & assigns reviewer
        self.client.login(username='editor@ppai.org.in', password='EditorPass123!')
        assign_response = self.client.post(
            reverse('editor_manuscript_review', kwargs={'tracking_id': manuscript.tracking_id}),
            {'assign_reviewer': '1', 'reviewer_id': str(self.reviewer_user.id), 'due_days': '21'},
            follow=True
        )
        self.assertEqual(assign_response.status_code, 200)

        assignment = ReviewAssignment.objects.get(manuscript=manuscript, reviewer=self.reviewer_user)
        self.assertEqual(assignment.status, 'pending')
        manuscript.refresh_from_db()
        self.assertEqual(manuscript.status, 'under_review')
        self.client.logout()

        # 3. Reviewer accepts invitation
        self.client.login(username='reviewer@icar.gov.in', password='ReviewerPass123!')
        accept_resp = self.client.get(
            reverse('reviewer_respond_invitation', kwargs={'assignment_id': assignment.id, 'response_action': 'accept'}),
            follow=True
        )
        self.assertEqual(accept_resp.status_code, 200)
        assignment.refresh_from_db()
        self.assertEqual(assignment.status, 'accepted')

        # 4. Reviewer evaluates manuscript (Comment on submitted manuscript by author)
        eval_resp = self.client.post(
            reverse('reviewer_evaluate_manuscript', kwargs={'assignment_id': assignment.id}),
            {
                'originality_score': 4,
                'technical_quality_score': 4,
                'clarity_score': 3,
                'significance_score': 4,
                'recommendation': 'minor_revision',
                'comments_for_author': 'Interesting methodology. Please elaborate on spore concentration metrics in Table 2.',
                'confidential_comments_to_editor': 'Sound paper, recommended with minor corrections.'
            },
            follow=True
        )
        self.assertEqual(eval_resp.status_code, 200)
        assignment.refresh_from_db()
        self.assertEqual(assignment.status, 'completed')
        manuscript.refresh_from_db()
        self.assertEqual(manuscript.status, 'review_completed')
        self.client.logout()

        # 5. Editor reviews feedback and issues decision: Return comments to Authors
        self.client.login(username='editor@ppai.org.in', password='EditorPass123!')
        decision_resp = self.client.post(
            reverse('editor_manuscript_review', kwargs={'tracking_id': manuscript.tracking_id}),
            {
                'submit_decision': '1',
                'decision': 'minor_revision',
                'comments_to_author': 'Please address Reviewer points regarding spore concentration in Table 2 and resubmit.',
                'internal_notes': 'Awaiting revised tables.'
            },
            follow=True
        )
        self.assertEqual(decision_resp.status_code, 200)
        manuscript.refresh_from_db()
        self.assertEqual(manuscript.status, 'revisions_requested')
        self.assertEqual(manuscript.editor_decision, 'minor_revision')
        self.client.logout()

        # 6. Author views comments and submits revised manuscript (Return comments to Authors response)
        self.client.login(username='author@university.edu', password='AuthorPass123!')
        rev_file = SimpleUploadedFile("revised_paper.docx", b"Revised manuscript with updated Table 2", content_type="application/msword")
        rev_resp = self.client.post(
            reverse('author_submit_revision', kwargs={'tracking_id': manuscript.tracking_id}),
            {
                'revised_file': rev_file,
                'response_to_reviewers': 'We have revised Table 2 and explicitly stated spore concentration at 1x10^8 CFU/ml.'
            },
            follow=True
        )
        self.assertEqual(rev_resp.status_code, 200)
        manuscript.refresh_from_db()
        self.assertEqual(manuscript.status, 'revised_submitted')
        self.assertEqual(manuscript.revisions.count(), 1)
        self.client.logout()

        # 7. Editor approves access: Final Acceptance
        self.client.login(username='editor@ppai.org.in', password='EditorPass123!')
        final_resp = self.client.post(
            reverse('editor_manuscript_review', kwargs={'tracking_id': manuscript.tracking_id}),
            {
                'submit_decision': '1',
                'decision': 'accept',
                'comments_to_author': 'We are pleased to approve access and accept your revised manuscript for publication in the Indian Journal of Plant Protection (IJPP)!',
                'internal_notes': 'Accepted for upcoming volume.'
            },
            follow=True
        )
        self.assertEqual(final_resp.status_code, 200)
        manuscript.refresh_from_db()
        self.assertEqual(manuscript.status, 'accepted')
        self.assertEqual(manuscript.editor_decision, 'accept')
        self.client.logout()
