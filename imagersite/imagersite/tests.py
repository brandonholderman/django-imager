from django.test import Client
from django.test import TestCase


class ViewTests(TestCase):
    """Testing each view controller"""

    def test_successful_login(self):
        """tests login is successful"""
        c = Client()
        response = c.post('/accounts/login/', {'username': 'john',
                                               'password': 'smith'})
        self.assertEqual(response.status_code, 200)

    def test_home_view(self):
        """tests successful retrieval of home view"""
        c = Client()
        reponse = c.get('/')
        self.assertEqual(reponse.status_code, 200)

    def test_admin_view(self):
        """tests successful retrieval of admin view"""
        c = Client()
        reponse = c.get('/admin/login/?next=/admin/')
        self.assertEqual(reponse.status_code, 200)

    def test_successful_logout(self):
        """test successfully logged out"""
        c = Client()
        response = c.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)

    def test_successful_account_signup(self):
        """test successful signup"""
        c = Client()
        response = c.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_registration_complete(self):
        """test successful registration"""
        c = Client()
        response = c.get('/accounts/register/complete/')
        self.assertEqual(response.status_code, 200)

    def test_activation_complete(self):
        """test successful activation complete"""
        c = Client()
        response = c.get('/accounts/activate/complete/')
        self.assertEqual(response.status_code, 200)
