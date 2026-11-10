from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from pages.models import ElectionRegistration
from pages.admin import generate_election_registrations_excel

class ElectionRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_election_button_present_in_base_header(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Election 2026', content)
        self.assertIn('btn-auth-election', content)
        # Verify Election 2026 is left side of Login in the header auth buttons
        election_idx = content.find('btn-auth-election')
        login_idx = content.find('btn-auth-login')
        self.assertNotEqual(election_idx, -1)
        self.assertNotEqual(login_idx, -1)
        self.assertLess(election_idx, login_idx)

    def test_election_registration_page_get(self):
        response = self.client.get(reverse('election_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/election_registration.html')
        content = response.content.decode('utf-8')
        # Check required texts & components
        self.assertIn('Membership Registration', content)
        self.assertIn('Indian Member', content)
        self.assertIn('Foreign Member', content)
        self.assertIn('Life', content)
        self.assertIn('Ordinary (Annual)', content)
        self.assertIn('Institutional (Annual)', content)
        self.assertIn('Students', content)
        self.assertIn('Registration Details', content)
        self.assertIn('Name', content)
        self.assertIn('Phone Number', content)
        self.assertIn('Email ID', content)
        self.assertIn('Designation', content)
        self.assertIn('Organization with Full Address', content)
        self.assertIn('Residence with Full Address', content)
        # Check that subtitle clutter paragraph is removed
        self.assertNotIn('Register your membership credentials for participation', content)
        # Check that center wrap submit button is used
        self.assertIn('el-submit-wrap', content)
        self.assertIn('el-submit-btn', content)

    def test_election_registration_post_success(self):
        payload = {
            'member_category': 'indian',
            'registration_type': 'life',
            'name': 'Dr. Suresh Kumar',
            'phone': '+91 9876543210',
            'email': 'suresh.kumar@icar.gov.in',
            'designation': 'Principal Scientist',
            'organization_address': 'ICAR - Indian Agricultural Research Institute, New Delhi - 110012',
            'residence_address': 'Flat 402, Scientist Enclave, Pusa Campus, New Delhi - 110012',
        }
        response = self.client.post(reverse('election_registration'), data=payload)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Membership Registration Submitted!', content)
        self.assertIn('PPAI-EL26-', content)
        self.assertIn('Dr. Suresh Kumar', content)

        # Verify database record
        self.assertEqual(ElectionRegistration.objects.count(), 1)
        reg = ElectionRegistration.objects.first()
        self.assertEqual(reg.name, 'Dr. Suresh Kumar')
        self.assertEqual(reg.member_category, 'indian')
        self.assertEqual(reg.registration_type, 'life')
        self.assertEqual(reg.email, 'suresh.kumar@icar.gov.in')

    def test_election_registration_foreign_member(self):
        payload = {
            'member_category': 'foreign',
            'registration_type': 'ordinary',
            'name': 'Dr. Jane Smith',
            'phone': '+1 555 123 4567',
            'email': 'jane.smith@cornell.edu',
            'designation': 'Associate Professor',
            'organization_address': 'Cornell University, Department of Plant Pathology, Ithaca, NY, USA',
            'residence_address': '123 University Ave, Ithaca, NY 14850, USA',
        }
        response = self.client.post(reverse('election_registration'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ElectionRegistration.objects.filter(member_category='foreign').count(), 1)
        reg = ElectionRegistration.objects.get(member_category='foreign')
        self.assertEqual(reg.get_member_category_display(), 'Foreign Member')
        self.assertEqual(reg.get_registration_type_display(), 'Ordinary (Annual)')

    def test_election_registration_validation_errors(self):
        # Empty payload
        response = self.client.post(reverse('election_registration'), data={})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Please resolve the following', content)
        self.assertIn('Name is required.', content)
        self.assertIn('Phone number is required.', content)
        self.assertIn('Email ID is required.', content)
        self.assertEqual(ElectionRegistration.objects.count(), 0)

    def test_admin_excel_export_action(self):
        ElectionRegistration.objects.create(
            member_category='indian',
            registration_type='life',
            name='Dr. Test Scientist',
            phone='9999999999',
            email='test@ppai.org.in',
            designation='Scientist',
            organization_address='Test Org',
            residence_address='Test Res'
        )
        qs = ElectionRegistration.objects.all()
        response = generate_election_registrations_excel(qs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        self.assertIn('PPAI_Election_2026_Registrations.xlsx', response['Content-Disposition'])
        self.assertGreater(len(response.content), 1000)

    def test_admin_excel_download_view(self):
        admin_user = User.objects.create_superuser('adminuser', 'admin@ppai.org.in', 'AdminPass123!')
        self.client.force_login(admin_user)
        response = self.client.get('/admin/pages/electionregistration/export-excel/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
