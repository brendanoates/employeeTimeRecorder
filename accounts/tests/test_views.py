from importlib import import_module

from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest
from django.test import Client, TestCase
from accounts.views import register as registration_page


class RegisterViewTest(TestCase):

    def test_registartion_page_contains_correct_html(self):
        # request = HttpRequest()
        # engine = import_module(settings.SESSION_ENGINE)
        # session_key = None
        # request.session = engine.SessionStore(session_key)
        client = Client()
        response = client.get(reverse('accounts:accounts-register'))
        self.assertTrue(response.content.startswith(b'<!doctype html>'))
        self.assertIn(b'<title>Registration</title>', response.content)
        self.assertIn(b'<label for="id_username">Username:</label>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
        response = client.post(reverse('accounts:accounts-register'),
                               {'username': 'testuser', 'password': 'testpassword'})
        self.assertContains(response, '', status_code=302)
        self.assertEqual(response.url, reverse('index')) #should redirect to index
        client.get(reverse('accounts:accounts-logout'))
        response = client.post(reverse('accounts:accounts-register'),
                               {'username': 'testuser', 'password': 'testpassword'})
        self.assertContains(response, 'This username has already been taken', status_code=200)
