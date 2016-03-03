from importlib import import_module

from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest
from django.test import Client, TestCase
from accounts.views import register as registration_page


class RegistrationPageTest(TestCase):
    def test_reverse_url_resolves_to_registration_page_view(self):
        found = resolve(reverse("accounts:accounts-register"))
        self.assertEqual(found.func, registration_page)

    def test_registartion_page_contains_correct_html(self):
        request = HttpRequest()
        engine = import_module(settings.SESSION_ENGINE)
        session_key = None
        request.session = engine.SessionStore(session_key)
        response = registration_page(request)
        self.assertTrue(response.content.startswith(b'<!doctype html>'))
        self.assertIn(b'<title>Registration</title>', response.content)
        self.assertIn(b'<label for="id_username">Username:</label>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))