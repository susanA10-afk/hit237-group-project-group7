from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomUserModelTest(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='adminuser',
            password='admin123',
            role='admin'
        )
        self.caseworker_user = User.objects.create_user(
            username='caseworker1',
            password='case123',
            role='caseworker'
        )

    def test_user_created_with_correct_role(self):
        self.assertEqual(self.admin_user.role, 'admin')
        self.assertEqual(self.caseworker_user.role, 'caseworker')

    def test_is_caseworker_returns_true(self):
        self.assertTrue(self.caseworker_user.is_caseworker())

    def test_is_caseworker_returns_false_for_admin(self):
        self.assertFalse(self.admin_user.is_caseworker())

    def test_is_admin_user_returns_true(self):
        self.assertTrue(self.admin_user.is_admin_user())

    def test_is_admin_user_returns_false_for_caseworker(self):
        self.assertFalse(self.caseworker_user.is_admin_user())

    def test_default_role_is_caseworker(self):
        user = User.objects.create_user(
            username='newuser',
            password='pass123'
        )
        self.assertEqual(user.role, 'caseworker')

    def test_str_returns_username_and_role(self):
        self.assertEqual(
            str(self.admin_user),
            "adminuser (admin)"
        )


class AuthenticationTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            role='caseworker'
        )

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)

    def test_logout_redirects_to_login(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_user_redirected_to_login(self):
        response = self.client.get(reverse('justice:youngperson-list'))
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login/', response.url)