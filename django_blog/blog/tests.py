from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthTests(TestCase):
    def test_user_registration_and_login(self):
        resp = self.client.post(reverse('blog:register'), {
            'username': 'tester',
            'email': 't@example.com',
            'password1': 'ComplexP@ssw0rd',
            'password2': 'ComplexP@ssw0rd',
        })
        self.assertEqual(resp.status_code, 302)  # redirect after register
        login = self.client.login(username='tester', password='ComplexP@ssw0rd')
        self.assertTrue(login)
