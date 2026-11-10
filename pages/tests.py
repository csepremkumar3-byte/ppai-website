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
        self.assertIn('Registration Type', content)
        self.assertIn('Life Member', content)
        self.assertIn('Annual Member', content)
        self.assertIn('Institutional Member', content)
        self.assertIn('Student Member', content)
        self.assertIn('Foreign Member', content)

        # Check that Membership Category cards are removed
        self.assertNotIn('el-category-card', content)
        self.assertNotIn('Membership Category', content)

        # Check that hint texts were removed as requested
        self.assertNotIn('e.g. 9876543210 or +91 9876543210', content)
        self.assertNotIn('Enter 6 numeric digits', content)

        # Check Organization Address fields from handwritten drawing
        self.assertIn('Org Name', content)
        self.assertIn('id_org_name', content)
        self.assertIn('id_org_address', content)
        self.assertIn('id_org_state', content)
        self.assertIn('id_org_city', content)
        self.assertIn('id_org_pincode', content)

        # Check Residential Address fields from handwritten drawing
        self.assertIn('Address 1', content)
        self.assertIn('id_res_address', content)
        self.assertIn('id_res_state', content)
        self.assertIn('id_res_city', content)
        self.assertIn('id_res_pincode', content)

        # Check that center wrap submit button is used
        self.assertIn('el-submit-wrap', content)
        self.assertIn('el-submit-btn', content)

    def test_election_registration_post_success(self):
        payload = {
            'registration_type': 'life',
            'name': 'Dr. Suresh Kumar',
            'phone': '9876543210',
            'email': 'suresh.kumar@icar.gov.in',
            'designation': 'Principal Scientist',
            'org_name': 'ICAR-IARI',
            'org_address': 'Pusa Campus',
            'org_state': 'Delhi (NCT)',
            'org_city': 'New Delhi',
            'org_pincode': '110012',
            'res_address': 'Flat 402, Scientist Enclave',
            'res_state': 'Delhi (NCT)',
            'res_city': 'New Delhi',
            'res_pincode': '110012',
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
        self.assertEqual(reg.registration_type, 'life')
        self.assertEqual(reg.get_registration_type_display(), 'Life Member')
        self.assertEqual(reg.phone, '9876543210')
        self.assertEqual(reg.email, 'suresh.kumar@icar.gov.in')
        self.assertEqual(reg.org_name, 'ICAR-IARI')
        self.assertEqual(reg.org_pincode, '110012')
        self.assertEqual(reg.res_pincode, '110012')

    def test_election_registration_foreign_member(self):
        payload = {
            'registration_type': 'foreign',
            'name': 'Dr. Jane Smith',
            'phone': '9876543210',
            'email': 'jane.smith@cornell.edu',
            'designation': 'Associate Professor',
            'org_name': 'Cornell University',
            'org_address': 'Department of Plant Pathology',
            'org_state': 'Other / International',
            'org_city': 'Ithaca',
            'org_pincode': '148500',
            'res_address': '123 University Ave',
            'res_state': 'Other / International',
            'res_city': 'Ithaca',
            'res_pincode': '148500',
        }
        response = self.client.post(reverse('election_registration'), data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ElectionRegistration.objects.filter(registration_type='foreign').count(), 1)
        reg = ElectionRegistration.objects.get(registration_type='foreign')
        self.assertEqual(reg.get_registration_type_display(), 'Foreign Member')
        self.assertEqual(reg.member_category, 'foreign')

    def test_election_registration_phone_10_digits_validation(self):
        # Test less than 10 digits
        payload = {
            'registration_type': 'annual',
            'name': 'Ramesh Verma',
            'phone': '98765',  # only 5 digits
            'email': 'ramesh@icar.gov.in',
            'designation': 'Scientist',
            'org_name': 'ICAR',
            'org_address': 'Campus',
            'org_state': 'Telangana',
            'org_city': 'Hyderabad',
            'org_pincode': '500030',
            'res_address': 'Street 1',
            'res_state': 'Telangana',
            'res_city': 'Hyderabad',
            'res_pincode': '500030',
        }
        response = self.client.post(reverse('election_registration'), data=payload)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Phone Number must be exactly 10 digits.', content)
        self.assertEqual(ElectionRegistration.objects.count(), 0)

    def test_election_registration_pincode_validation(self):
        # Invalid 4-digit pincode
        payload = {
            'registration_type': 'annual',
            'name': 'Ramesh Verma',
            'phone': '9876543210',
            'email': 'ramesh@icar.gov.in',
            'designation': 'Scientist',
            'org_name': 'ICAR',
            'org_address': 'Campus',
            'org_state': 'Telangana',
            'org_city': 'Hyderabad',
            'org_pincode': '1234',  # invalid
            'res_address': 'Street 1',
            'res_state': 'Telangana',
            'res_city': 'Hyderabad',
            'res_pincode': '500030',
        }
        response = self.client.post(reverse('election_registration'), data=payload)
        self.assertEqual(response.status_code, 200)
        content = response.content.decode('utf-8')
        self.assertIn('Organization PIN Code must be exactly 6 numeric digits.', content)
        self.assertEqual(ElectionRegistration.objects.count(), 0)

    def test_admin_excel_export_action(self):
        ElectionRegistration.objects.create(
            registration_type='life',
            name='Dr. Test Scientist',
            phone='9999999999',
            email='test@ppai.org.in',
            designation='Scientist',
            org_name='Test Org',
            org_address='Test Address',
            org_city='Hyderabad',
            org_state='Telangana',
            org_pincode='500030',
            res_address='Test Res',
            res_city='Hyderabad',
            res_state='Telangana',
            res_pincode='500030'
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
