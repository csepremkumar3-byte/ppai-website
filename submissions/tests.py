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

    def test_01_portal_login_redirections(self):
        """Test role-based redirection upon login."""
        # Author login -> author_dashboard
        response = self.client.post(reverse('portal_login'), {
            'email': 'author@university.edu',
            'password': 'AuthorPass123!'
        }, follow=True)
        self.assertRedirects(response, reverse('author_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Author')
        self.client.logout()

        # Reviewer login -> reviewer_dashboard
        response = self.client.post(reverse('portal_login'), {
            'email': 'reviewer@icar.gov.in',
            'password': 'ReviewerPass123!'
        }, follow=True)
        self.assertRedirects(response, reverse('reviewer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Peer Reviewer')
        self.client.logout()

        # Editor login -> editor_dashboard
        response = self.client.post(reverse('portal_login'), {
            'email': 'editor@ppai.org.in',
            'password': 'EditorPass123!'
        }, follow=True)
        self.assertRedirects(response, reverse('editor_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editor Command Center')
        self.client.logout()

    def test_02_author_manuscript_submission(self):
        """Author submits a manuscript with metadata and DOCX attachment."""
        self.client.login(username='author@university.edu', password='AuthorPass123!')

        test_doc = SimpleUploadedFile(
            "novel_biopesticide_study.docx",
            b"PK\x03\x04Mock Word DOCX Content for Agricultural Research",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

        response = self.client.post(reverse('submit_manuscript'), {
            'article_type': 'research_article',
            'subject_area': 'entomology',
            'title': 'Efficacy of Indigenous Entomopathogenic Fungi Against Spodoptera frugiperda in Maize Ecosystems',
            'abstract': 'Fall armyworm causes catastrophic yield losses. This study evaluated native Beauveria bassiana strains.',
            'keywords': 'Spodoptera frugiperda, Beauveria bassiana, biological control, maize, LC50',
            'co_authors': 'Dr. K. Patel, UAS Dharwad',
            'manuscript_file': test_doc,
            'cover_letter': 'We submit this original research for consideration in IJPP.',
            'conflict_of_interest': True
        }, follow=True)

        self.assertEqual(response.status_code, 200)
        manuscript = Manuscript.objects.first()
        self.assertIsNotNone(manuscript)
        self.assertTrue(manuscript.tracking_id.startswith('IJPP-'))
        self.assertEqual(manuscript.status, 'submitted')
        self.assertEqual(manuscript.author, self.author_user)
        self.assertContains(response, manuscript.tracking_id)

    def test_03_full_peer_review_and_editorial_loop(self):
        """End-to-End: Submission -> Editor assigns Reviewer -> Reviewer scores -> Editor requests Revision -> Author resubmits -> Final Acceptance."""
        # 1. Author submits manuscript
        dummy_file = SimpleUploadedFile("paper.docx", b"Manuscript content", content_type="application/msword")
        manuscript = Manuscript.objects.create(
            author=self.author_user,
            title="Bio-efficacy of Trichoderma harzianum on Rhizoctonia solani",
            abstract="Study on biological control of sheath blight.",
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

        # 4. Reviewer evaluates manuscript (scores rubric, comments for author, confidential notes)
        eval_resp = self.client.post(
            reverse('reviewer_evaluate_manuscript', kwargs={'assignment_id': assignment.id}),
            {
                'originality_score': 4,
                'technical_quality_score': 4,
                'clarity_score': 3,
                'significance_score': 4,
                'recommendation': 'minor_revision',
                'comments_for_author': 'Interesting methodology. Please elaborate on the spore concentration metrics in Table 2.',
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

        # 5. Editor reviews feedback and issues decision: Request Minor Revision
        self.client.login(username='editor@ppai.org.in', password='EditorPass123!')
        decision_resp = self.client.post(
            reverse('editor_manuscript_review', kwargs={'tracking_id': manuscript.tracking_id}),
            {
                'submit_decision': '1',
                'decision': 'minor_revision',
                'comments_to_author': 'Please address Reviewer 1 points regarding spore concentration and resubmit.',
                'internal_notes': 'Awaiting revised tables.'
            },
            follow=True
        )
        self.assertEqual(decision_resp.status_code, 200)
        manuscript.refresh_from_db()
        self.assertEqual(manuscript.status, 'revisions_requested')
        self.assertEqual(manuscript.editor_decision, 'minor_revision')
        self.client.logout()

        # 6. Author views comments and submits revised manuscript
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

        # 7. Editor approves final revised paper: Accept
        self.client.login(username='editor@ppai.org.in', password='EditorPass123!')
        final_resp = self.client.post(
            reverse('editor_manuscript_review', kwargs={'tracking_id': manuscript.tracking_id}),
            {
                'submit_decision': '1',
                'decision': 'accept',
                'comments_to_author': 'We are pleased to accept your revised manuscript for publication in the Indian Journal of Plant Protection!',
                'internal_notes': 'Accepted for upcoming volume.'
            },
            follow=True
        )
        self.assertEqual(final_resp.status_code, 200)
        manuscript.refresh_from_db()
        self.assertEqual(manuscript.status, 'accepted')
        self.assertEqual(manuscript.editor_decision, 'accept')
        self.client.logout()
