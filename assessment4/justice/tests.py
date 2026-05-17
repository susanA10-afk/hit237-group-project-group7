from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import YoungPerson, Offence, Intervention, CaseWorker
from .services import (
    get_all_young_persons,
    get_high_risk_cases,
    get_young_person_by_id,
    record_offence,
    assign_intervention,
    get_dashboard_stats
)
from .exceptions import YoungPersonNotFound, InterventionLimitExceeded

User = get_user_model()


class YoungPersonModelTest(TestCase):

    def setUp(self):
        self.high_risk = YoungPerson.objects.create(
            first_name="John",
            last_name="Smith",
            date_of_birth="2005-01-01",
            gender="Male",
            postcode="0800",
            risk_level="high"
        )
        self.low_risk = YoungPerson.objects.create(
            first_name="Jane",
            last_name="Doe",
            date_of_birth="2006-01-01",
            gender="Female",
            postcode="0810",
            risk_level="low"
        )

    def test_high_risk_manager_returns_only_high_risk(self):
        result = YoungPerson.high_risk.all()
        self.assertIn(self.high_risk, result)
        self.assertNotIn(self.low_risk, result)

    def test_is_high_risk_returns_true_for_high(self):
        self.assertTrue(self.high_risk.is_high_risk())

    def test_is_high_risk_returns_false_for_low(self):
        self.assertFalse(self.low_risk.is_high_risk())

    def test_age_calculated_correctly(self):
        from datetime import date
        expected_age = date.today().year - 2005
        self.assertEqual(self.high_risk.age, expected_age)

    def test_str_returns_full_name(self):
        self.assertEqual(str(self.high_risk), "John Smith")


class RecordOffenceServiceTest(TestCase):

    def setUp(self):
        self.person = YoungPerson.objects.create(
            first_name="John",
            last_name="Smith",
            date_of_birth="2005-01-01",
            gender="Male",
            postcode="0800",
            risk_level="low"
        )

    def test_serious_offence_updates_risk_to_high(self):
        record_offence(self.person.pk, {
            'offence_type': 'Assault',
            'date_of_offence': '2024-01-01',
            'location': 'Darwin',
            'severity': 'serious',
            'description': 'Test offence'
        })
        self.person.refresh_from_db()
        self.assertEqual(self.person.risk_level, 'high')

    def test_minor_offence_does_not_change_risk(self):
        record_offence(self.person.pk, {
            'offence_type': 'Theft',
            'date_of_offence': '2024-01-01',
            'location': 'Darwin',
            'severity': 'minor',
            'description': 'Test offence'
        })
        self.person.refresh_from_db()
        self.assertEqual(self.person.risk_level, 'low')

    def test_invalid_person_raises_exception(self):
        with self.assertRaises(YoungPersonNotFound):
            record_offence(99999, {
                'offence_type': 'Theft',
                'date_of_offence': '2024-01-01',
                'location': 'Darwin',
                'severity': 'minor',
                'description': 'Test'
            })


class GetYoungPersonServiceTest(TestCase):

    def setUp(self):
        self.person = YoungPerson.objects.create(
            first_name="John",
            last_name="Smith",
            date_of_birth="2005-01-01",
            gender="Male",
            postcode="0800",
            risk_level="high"
        )

    def test_get_young_person_by_id_returns_correct_person(self):
        result = get_young_person_by_id(self.person.pk)
        self.assertEqual(result, self.person)

    def test_get_young_person_with_invalid_id_raises_exception(self):
        with self.assertRaises(YoungPersonNotFound):
            get_young_person_by_id(99999)


class DashboardStatsTest(TestCase):

    def setUp(self):
        YoungPerson.objects.create(
            first_name="John", last_name="Smith",
            date_of_birth="2005-01-01", gender="Male",
            postcode="0800", risk_level="high"
        )
        YoungPerson.objects.create(
            first_name="Jane", last_name="Doe",
            date_of_birth="2006-01-01", gender="Female",
            postcode="0810", risk_level="low"
        )

    def test_stats_returns_correct_total(self):
        stats = get_dashboard_stats()
        self.assertEqual(stats['total_young_persons'], 2)

    def test_stats_returns_correct_high_risk_count(self):
        stats = get_dashboard_stats()
        self.assertEqual(stats['high_risk_count'], 1)


class LoginRequiredTest(TestCase):

    def setUp(self):
        self.client = Client()

    def test_young_person_list_requires_login(self):
        response = self.client.get(reverse('justice:youngperson-list'))
        self.assertEqual(response.status_code, 302)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse('justice:dashboard'))
        self.assertEqual(response.status_code, 302)

    def test_stats_requires_login(self):
        response = self.client.get(reverse('justice:stats'))
        self.assertEqual(response.status_code, 302)


class AuthenticatedViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.client.login(username='testuser', password='testpass123')
        self.person = YoungPerson.objects.create(
            first_name="John", last_name="Smith",
            date_of_birth="2005-01-01", gender="Male",
            postcode="0800", risk_level="high"
        )

    def test_logged_in_user_can_access_list(self):
        response = self.client.get(reverse('justice:youngperson-list'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_access_detail(self):
        response = self.client.get(
            reverse('justice:youngperson-detail', args=[self.person.pk])
        )
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_access_dashboard(self):
        response = self.client.get(reverse('justice:dashboard'))
        self.assertEqual(response.status_code, 200)

class InterventionLimitTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='worker', password='pass123'
        )
        self.caseworker = CaseWorker.objects.create(
            user=self.user,
            employee_id='EMP001',
            phone='0400000000',
            department='Justice'
        )
        self.person = YoungPerson.objects.create(
            first_name="John", last_name="Smith",
            date_of_birth="2005-01-01", gender="Male",
            postcode="0800", risk_level="high"
        )

    def test_intervention_limit_exceeded_raises_exception(self):
        for i in range(3):
            assign_intervention(self.person.pk, self.caseworker, {
                'intervention_type': f'Type {i}',
                'start_date': '2024-01-01',
                'status': 'active',
                'outcome': ''
            })
        with self.assertRaises(InterventionLimitExceeded):
            assign_intervention(self.person.pk, self.caseworker, {
                'intervention_type': 'One too many',
                'start_date': '2024-01-01',
                'status': 'active',
                'outcome': ''
            })