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
            affiliation='PPAI Editorial Office'
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

        # 4. Setup Admin / Superuser
        self.admin_user = User.objects.create_superuser(
            username='admin@ppai.org.in',
            email='admin@ppai.org.in',
            password='AdminPass123!',
            first_name='System',
            last_name='Administrator'
        )
        self.admin_profile = UserProfile.objects.create(
            user=self.admin_user,
            role='admin',
            is_editor=False,
            affiliation='PPAI Central Office'
        )

    def test_01_existing_login_and_role_based_access(self):
        """Test role-based access redirection using existing /login/ endpoint."""
        # Admin login -> admin_dashboard
        response = self.client.post(reverse('login'), {
            'email': 'admin@ppai.org.in',
            'password': 'AdminPass123!'
        }, follow=True)
        self.assertRedirects(response, reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Chief Editor Console')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Associate Editor')
        self.assertContains(response, 'Reviewer')
        self.assertNotContains(response, 'Administrator Command Center')
        self.assertNotContains(response, 'Django Admin')
        self.client.logout()

        # Author login -> author_dashboard
        response = self.client.post(reverse('login'), {
            'email': 'author@university.edu',
            'password': 'AuthorPass123!'
        }, follow=True)
        self.assertRedirects(response, reverse('author_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Plant Protection Association of India')
        self.assertContains(response, 'Submitted Manuscripts')
        self.client.logout()

        # Reviewer login -> reviewer_dashboard
        response = self.client.post(reverse('login'), {
            'email': 'reviewer@icar.gov.in',
            'password': 'ReviewerPass123!'
        }, follow=True)
        self.assertRedirects(response, reverse('reviewer_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Reviewer')
        self.assertContains(response, 'Reviewer Console')
        self.assertContains(response, 'New Reviewer Assignments')
        self.assertContains(response, 'Pending Assignment')
        self.assertContains(response, 'Complete Assignments')
        self.assertContains(response, 'Review Instructions')
        self.assertContains(response, 'Feedback for the Authors')
        self.assertContains(response, 'Your Assignments')
        self.client.logout()

        # Editor login -> editor_dashboard
        response = self.client.post(reverse('login'), {
            'email': 'editor@ppai.org.in',
            'password': 'EditorPass123!'
        }, follow=True)
        self.assertRedirects(response, reverse('editor_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Editorial Manuscripts')
        self.client.logout()

    def test_02_author_registration_and_validation(self):
        """Test public Author registration with strict email and password validation, and backoffice role login."""
        # 1. Invalid email format rejection
        resp_invalid_email = self.client.post(reverse('register'), {
            'full_name': 'Dr. Test Author',
            'email': 'not-an-email',
            'affiliation': 'ICAR-IIHR Bangalore',
            'password': 'Password123!',
            'confirm_password': 'Password123!'
        })
        self.assertEqual(resp_invalid_email.status_code, 200)
        self.assertContains(resp_invalid_email, 'Please enter a valid email address')

        # 2. Password length rejection (< 8 characters)
        resp_short_pwd = self.client.post(reverse('register'), {
            'full_name': 'Dr. Test Author',
            'email': 'valid.author@icar.gov.in',
            'affiliation': 'ICAR-IIHR Bangalore',
            'password': 'Pass1',
            'confirm_password': 'Pass1'
        })
        self.assertEqual(resp_short_pwd.status_code, 200)
        self.assertContains(resp_short_pwd, 'Password must be at least 8 characters long')

        # 3. Password letters & numbers requirement
        resp_alpha_only = self.client.post(reverse('register'), {
            'full_name': 'Dr. Test Author',
            'email': 'valid.author@icar.gov.in',
            'affiliation': 'ICAR-IIHR Bangalore',
            'password': 'OnlyLettersPassword',
            'confirm_password': 'OnlyLettersPassword'
        })
        self.assertEqual(resp_alpha_only.status_code, 200)
        self.assertContains(resp_alpha_only, 'Password must contain both letters and numbers')

        # 3b. Password uppercase letter requirement
        resp_no_upper = self.client.post(reverse('register'), {
            'full_name': 'Dr. Test Author',
            'email': 'valid.author@icar.gov.in',
            'affiliation': 'ICAR-IIHR Bangalore',
            'password': 'nouppercasepassword123',
            'confirm_password': 'nouppercasepassword123'
        })
        self.assertEqual(resp_no_upper.status_code, 200)
        self.assertContains(resp_no_upper, 'Password must contain at least one uppercase letter')

        # 4. Passwords mismatch rejection
        resp_mismatch = self.client.post(reverse('register'), {
            'full_name': 'Dr. Test Author',
            'email': 'valid.author@icar.gov.in',
            'affiliation': 'ICAR-IIHR Bangalore',
            'password': 'Password123!',
            'confirm_password': 'DifferentPass123!'
        })
        self.assertEqual(resp_mismatch.status_code, 200)
        self.assertContains(resp_mismatch, 'Passwords do not match')

        # 5. Successful Author Registration -> Redirects to login with success message
        resp_author = self.client.post(reverse('register'), {
            'full_name': 'Dr. Arun Kumar',
            'email': 'arun.author@icar.gov.in',
            'affiliation': 'ICAR-IIHR Bangalore',
            'password': 'SecretPass123!',
            'confirm_password': 'SecretPass123!'
        }, follow=True)
        self.assertRedirects(resp_author, reverse('login'))
        self.assertContains(resp_author, 'Author registration successful')
        self.assertTrue(User.objects.filter(email='arun.author@icar.gov.in').exists())

        # Duplicate email registration rejected
        resp_dup = self.client.post(reverse('register'), {
            'full_name': 'Another User',
            'email': 'arun.author@icar.gov.in',
            'affiliation': 'Different Org',
            'password': 'SecretPass123!',
            'confirm_password': 'SecretPass123!'
        })
        self.assertContains(resp_dup, 'An account with this email address already exists')

        # Author logs in -> Redirects directly to Author Dashboard
        login_author = self.client.post(reverse('login'), {
            'email': 'arun.author@icar.gov.in',
            'password': 'SecretPass123!'
        }, follow=True)
        self.assertRedirects(login_author, reverse('author_dashboard'))
        self.client.logout()

        # 6. Backoffice / Admin provisioned Reviewer logs in -> Redirects to Reviewer Dashboard
        rev_admin_user = User.objects.create_user(
            username='admin.reviewer@university.edu',
            email='admin.reviewer@university.edu',
            password='ReviewerPass123!',
            first_name='Prof.',
            last_name='Raman'
        )
        UserProfile.objects.create(
            user=rev_admin_user,
            role='reviewer',
            is_reviewer=True,
            affiliation='TNAU Coimbatore'
        )
        login_reviewer = self.client.post(reverse('login'), {
            'email': 'admin.reviewer@university.edu',
            'password': 'ReviewerPass123!'
        }, follow=True)
        self.assertRedirects(login_reviewer, reverse('reviewer_dashboard'))
        self.client.logout()

        # 7. Backoffice / Admin provisioned Editor logs in -> Redirects to Editor Dashboard
        ed_admin_user = User.objects.create_user(
            username='admin.editor@ppai.org.in',
            email='admin.editor@ppai.org.in',
            password='EditorPass123!',
            first_name='Dr.',
            last_name='Editorial'
        )
        UserProfile.objects.create(
            user=ed_admin_user,
            role='editor',
            is_editor=True,
            affiliation='PPAI Editorial Office'
        )
        login_editor = self.client.post(reverse('login'), {
            'email': 'admin.editor@ppai.org.in',
            'password': 'EditorPass123!'
        }, follow=True)
        self.assertRedirects(login_editor, reverse('editor_dashboard'))
        self.client.logout()

    def test_03_full_paper_flow_loop_and_editor_approval_release(self):
        """End-to-End Paper Flow:
        Register -> Login -> Author manuscript submission -> Editor (view and edit) then approve access ->
        Reviewer (view and edit access) -> Comment on submitted manuscript by author (goes to editor first) ->
        Editor approves -> Return comments to Authors -> Revision -> Acceptance
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
        self.assertTrue(manuscript.tracking_id.startswith(('PPAI-', 'IJPP-')))

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

        # Reviewer visits evaluation workspace via card
        eval_get = self.client.get(reverse('reviewer_evaluate_manuscript', kwargs={'assignment_id': assignment.id}))
        self.assertEqual(eval_get.status_code, 200)
        self.assertContains(eval_get, 'Review Status')
        self.assertContains(eval_get, 'Manuscript Information')
        self.assertContains(eval_get, 'Manuscript Files')
        self.assertContains(eval_get, 'Overall Recommendation')
        self.assertContains(eval_get, 'Comments for Author')
        self.assertContains(eval_get, 'Confidential Remarks for Associate Editor Only')

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
        self.assertFalse(assignment.is_approved_by_editor)  # Held with Editor first!
        manuscript.refresh_from_db()
        self.assertEqual(manuscript.status, 'review_completed')
        self.client.logout()

        # Verify: comments done by reviewer go to editor first (Author CANNOT see them yet!)
        self.client.login(username='author@university.edu', password='AuthorPass123!')
        author_view_pre = self.client.get(reverse('author_manuscript_detail', kwargs={'tracking_id': manuscript.tracking_id}))
        self.assertEqual(author_view_pre.status_code, 200)
        self.assertNotContains(author_view_pre, 'Interesting methodology. Please elaborate on spore concentration metrics in Table 2.')
        self.assertContains(author_view_pre, 'Review Completed &mdash; With Editor')
        self.client.logout()

        # 5. Editor reviews feedback, APPROVES reviewer comments, and issues decision: Return comments to Authors
        self.client.login(username='editor@ppai.org.in', password='EditorPass123!')
        decision_resp = self.client.post(
            reverse('editor_manuscript_review', kwargs={'tracking_id': manuscript.tracking_id}),
            {
                'submit_decision': '1',
                'decision': 'minor_revision',
                'approve_reviewer_comments': '1',  # Editor approves comments to go to author!
                'comments_to_author': 'Please address Reviewer points regarding spore concentration in Table 2 and resubmit.',
                'internal_notes': 'Awaiting revised tables.'
            },
            follow=True
        )
        self.assertEqual(decision_resp.status_code, 200)
        assignment.refresh_from_db()
        self.assertTrue(assignment.is_approved_by_editor)  # Now approved by editor!
        manuscript.refresh_from_db()
        self.assertEqual(manuscript.status, 'revisions_requested')
        self.assertEqual(manuscript.editor_decision, 'minor_revision')
        self.client.logout()

        # 6. Author visits after Editor approves: Reviewer comments are NOW visible to Author!
        self.client.login(username='author@university.edu', password='AuthorPass123!')
        author_view_post = self.client.get(reverse('author_manuscript_detail', kwargs={'tracking_id': manuscript.tracking_id}))
        self.assertEqual(author_view_post.status_code, 200)
        self.assertContains(author_view_post, 'Interesting methodology. Please elaborate on spore concentration metrics in Table 2.')

        # Author submits revised manuscript (Return comments to Authors response)
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
                'approve_reviewer_comments': '1',
                'comments_to_author': 'We are pleased to approve access and accept your revised manuscript for publication in the Plant Protection Association of India (PPAI)!',
                'internal_notes': 'Accepted for upcoming volume.'
            },
            follow=True
        )
        self.assertEqual(final_resp.status_code, 200)
        manuscript.refresh_from_db()
        self.assertEqual(manuscript.status, 'accepted')
        self.assertEqual(manuscript.editor_decision, 'accept')
        self.client.logout()

    def test_04_admin_dashboard_user_management(self):
        """Test Admin Dashboard creation of Editors and Reviewers, and user deletion."""
        # Login as Admin
        self.client.login(username='admin@ppai.org.in', password='AdminPass123!')
        dash_resp = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(dash_resp.status_code, 200)
        self.assertContains(dash_resp, 'Chief Editor Console')
        self.assertContains(dash_resp, 'Register')
        self.assertContains(dash_resp, 'Associate Editor')
        self.assertContains(dash_resp, 'Reviewer')

        # Verify clutter texts and Editor Panel have been removed
        self.assertNotContains(dash_resp, 'Administrator Command Center')
        self.assertNotContains(dash_resp, 'Django Admin')
        self.assertNotContains(dash_resp, 'Editor Panel')
        self.assertNotContains(dash_resp, 'Share this password with the user')
        self.assertNotContains(dash_resp, 'All active accounts across Author, Reviewer, and Editorial roles')

        # Verify Admin is NOT counted as an editor
        self.assertEqual(dash_resp.context['counts']['editors'], 1)  # Only self.editor_user from setUp, NOT admin

        # Admin trying to access editor dashboard is redirected to admin_dashboard
        editor_access_resp = self.client.get(reverse('editor_dashboard'))
        self.assertRedirects(editor_access_resp, reverse('admin_dashboard'))

        # Password without uppercase rejection in admin dashboard
        resp_no_upper = self.client.post(reverse('admin_dashboard'), {
            'action': 'create_user',
            'role': 'editor',
            'full_name': 'Dr. No Upper',
            'email': 'noupper.editor@ppai.org.in',
            'affiliation': 'ICAR',
            'password': 'nouppercasepass123'
        }, follow=True)
        self.assertContains(resp_no_upper, 'Password must contain at least one uppercase letter')

        # 1. Admin creates an Editor
        create_editor_resp = self.client.post(reverse('admin_dashboard'), {
            'action': 'create_user',
            'role': 'editor',
            'full_name': 'Prof. Anita Sharma',
            'email': 'anita.editor@ppai.org.in',
            'affiliation': 'ICAR-NCIPM, New Delhi',
            'specialization': 'Plant Virology',
            'password': 'AnitaPass123!'
        }, follow=True)
        self.assertEqual(create_editor_resp.status_code, 200)
        self.assertContains(create_editor_resp, 'Successfully registered Associate Editor: Prof. Anita Sharma')

        # 2. Admin creates a Reviewer
        create_rev_resp = self.client.post(reverse('admin_dashboard'), {
            'action': 'create_user',
            'role': 'reviewer',
            'full_name': 'Dr. Vikram Patel',
            'email': 'vikram.reviewer@icar.gov.in',
            'affiliation': 'ICAR-IARI, New Delhi',
            'specialization': 'Mycology',
            'password': 'VikramPass123!'
        }, follow=True)
        self.assertEqual(create_rev_resp.status_code, 200)
        self.assertContains(create_rev_resp, 'Successfully registered Reviewer: Dr. Vikram Patel')

        # Filter check
        filter_resp = self.client.get(reverse('admin_dashboard') + '?role=reviewer')
        self.assertEqual(filter_resp.status_code, 200)
        self.assertContains(filter_resp, 'vikram.reviewer@icar.gov.in')

        self.client.logout()

        # 3. Newly created Editor logs in -> routes to editor_dashboard
        login_editor = self.client.post(reverse('login'), {
            'email': 'anita.editor@ppai.org.in',
            'password': 'AnitaPass123!'
        }, follow=True)
        self.assertRedirects(login_editor, reverse('editor_dashboard'))
        self.client.logout()

        # 4. Newly created Reviewer logs in -> routes to reviewer_dashboard
        login_reviewer = self.client.post(reverse('login'), {
            'email': 'vikram.reviewer@icar.gov.in',
            'password': 'VikramPass123!'
        }, follow=True)
        self.assertRedirects(login_reviewer, reverse('reviewer_dashboard'))
        self.client.logout()

        # 5. Admin deletes user
        self.client.login(username='admin@ppai.org.in', password='AdminPass123!')
        vikram_user = User.objects.get(email='vikram.reviewer@icar.gov.in')
        del_resp = self.client.get(reverse('admin_delete_user', kwargs={'user_id': vikram_user.id}), follow=True)
        self.assertEqual(del_resp.status_code, 200)
        self.assertContains(del_resp, "was successfully deleted")
        self.assertFalse(User.objects.filter(email='vikram.reviewer@icar.gov.in').exists())
        self.client.logout()

    def test_16_upload_5mb_validation_and_password_toggle(self):
        """Test that file uploads enforce 5MB maximum limit, and password fields have privacy toggle."""
        from django.core.exceptions import ValidationError
        from submissions.forms import validate_file_extension, ManuscriptSubmissionForm

        # 1. 6MB file rejected by validate_file_extension
        large_file = SimpleUploadedFile("oversized.pdf", b"x" * (6 * 1024 * 1024), content_type="application/pdf")
        with self.assertRaises(ValidationError) as ctx:
            validate_file_extension(large_file)
        self.assertIn("5MB", str(ctx.exception))

        # 2. 1MB file accepted
        valid_file = SimpleUploadedFile("valid.pdf", b"x" * (1024 * 1024), content_type="application/pdf")
        try:
            validate_file_extension(valid_file)
        except ValidationError:
            self.fail("validate_file_extension raised ValidationError unexpectedly for 1MB file!")

        # 3. Check login and register pages render password privacy toggle button
        resp_login = self.client.get(reverse('login'))
        self.assertContains(resp_login, 'password-toggle-btn')
        self.assertContains(resp_login, 'togglePasswordVisibility')

        resp_register = self.client.get(reverse('register'))
        self.assertContains(resp_register, 'password-toggle-btn')
        self.assertContains(resp_register, 'togglePasswordVisibility')

        # 4. Check submit manuscript and submit revision templates render 5MB hints
        self.client.force_login(self.author_user)
        resp_submit = self.client.get(reverse('submit_manuscript'))
        self.assertEqual(resp_submit.status_code, 200)
        self.assertContains(resp_submit, '5MB')

        m = Manuscript.objects.create(
            author=self.author_user,
            title="Bio-efficacy test",
            abstract="Abstract content",
            keywords="test",
            status="revisions_requested"
        )
        resp_rev = self.client.get(reverse('author_submit_revision', kwargs={'tracking_id': m.tracking_id}))
        self.assertEqual(resp_rev.status_code, 200)
        self.assertContains(resp_rev, '5MB')
        self.assertNotContains(resp_rev, '30MB')
        self.client.logout()

    def test_17_chief_editor_console_workflow_stats_and_table(self):
        """Test Chief Editor Console manuscript stats (7 workflow states) and uncluttered table."""
        # Create manuscripts across various workflow statuses
        m_received = Manuscript.objects.create(
            author=self.author_user,
            title="Received Manuscript Title",
            abstract="Abstract 1",
            status="submitted"
        )
        m_under_review = Manuscript.objects.create(
            author=self.author_user,
            title="Under Review Manuscript Title",
            abstract="Abstract 2",
            status="under_review"
        )
        m_2nd_review = Manuscript.objects.create(
            author=self.author_user,
            title="Under 2nd Review Manuscript Title",
            abstract="Abstract 3",
            status="revised_submitted"
        )
        m_sent_back = Manuscript.objects.create(
            author=self.author_user,
            title="Sent Back Manuscript Title",
            abstract="Abstract 4",
            status="revisions_requested"
        )
        m_accepted = Manuscript.objects.create(
            author=self.author_user,
            title="Accepted Manuscript Title",
            abstract="Abstract 5",
            status="accepted"
        )
        m_rejected = Manuscript.objects.create(
            author=self.author_user,
            title="Rejected Manuscript Title",
            abstract="Abstract 6",
            status="rejected"
        )
        m_published = Manuscript.objects.create(
            author=self.author_user,
            title="Published Manuscript Title",
            abstract="Abstract 7",
            status="published"
        )

        # Log in as Chief Editor
        self.client.login(username='admin@ppai.org.in', password='AdminPass123!')
        resp = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(resp.status_code, 200)

        # 1. Verify 7 workflow stats are present in context
        stats = resp.context['manuscript_stats']
        self.assertEqual(stats['received'], 1)
        self.assertEqual(stats['under_review'], 1)
        self.assertEqual(stats['under_2nd_review'], 1)
        self.assertEqual(stats['sent_back_to_author'], 1)
        self.assertEqual(stats['accepted'], 1)
        self.assertEqual(stats['rejected'], 1)
        self.assertEqual(stats['published'], 1)

        # 2. Verify stats cards and table column headers in HTML
        self.assertContains(resp, 'Received')
        self.assertContains(resp, 'Under Review')
        self.assertContains(resp, 'Under 2nd Review')
        self.assertContains(resp, 'Sent Back to Author')
        self.assertContains(resp, 'Accepted')
        self.assertContains(resp, 'Rejected')
        self.assertContains(resp, 'Published')

        # Verify table column headers
        self.assertContains(resp, 'Current Status')
        self.assertContains(resp, 'Date of Submission')
        self.assertContains(resp, 'Last Updated')

        # 3. Verify status filtering works
        resp_filter_rec = self.client.get(reverse('admin_dashboard') + '?status=received')
        self.assertEqual(len(resp_filter_rec.context['manuscripts']), 1)
        self.assertEqual(resp_filter_rec.context['manuscripts'][0].tracking_id, m_received.tracking_id)

        resp_filter_pub = self.client.get(reverse('admin_dashboard') + '?status=published')
        self.assertEqual(len(resp_filter_pub.context['manuscripts']), 1)
        self.assertEqual(resp_filter_pub.context['manuscripts'][0].tracking_id, m_published.tracking_id)

        # 4. Verify search filtering works
        resp_search = self.client.get(reverse('admin_dashboard') + f'?q={m_accepted.tracking_id}')
        self.assertEqual(len(resp_search.context['manuscripts']), 1)
        self.assertEqual(resp_search.context['manuscripts'][0].tracking_id, m_accepted.tracking_id)
        self.client.logout()


