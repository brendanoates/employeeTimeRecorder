from importlib import import_module

from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest
from django.test import Client, TestCase

from accounts.views import register as registration_page
from accounts.views import login as accounts_login
from accounts.views import logout as accounts_logout
from accounts.views import password_change
from accounts.views import password_change_done
from accounts.views import password_reset
from accounts.views import password_reset_done
from accounts.views import password_reset_complete
from accounts.views import password_reset_confirm


class PageTests(TestCase):

    def test_reverse_url_resolves_to_registration_page_view(self):
        found = resolve(reverse("accounts:accounts-register"))
        self.assertEqual(found.func, registration_page)

    def test_reverse_url_resolves_to_accounts_login_view(self):
        found = resolve(reverse("accounts:accounts-login"))
        self.assertEqual(found.func, accounts_login)

    def test_reverse_url_resolves_to_accounts_logout_view(self):
        found = resolve(reverse("accounts:accounts-logout"))
        self.assertEqual(found.func, accounts_logout)

    def test_reverse_url_resolves_to_password_change_view(self):
        found = resolve(reverse("accounts:password-change"))
        self.assertEqual(found.func, password_change)

    def test_reverse_url_resolves_to_password_change_done_view(self):
        found = resolve(reverse("accounts:password-change-done"))
        self.assertEqual(found.func, password_change_done)

    def test_reverse_url_resolves_to_password_reset_view(self):
        found = resolve(reverse("accounts:password-reset"))
        self.assertEqual(found.func, password_reset)

    def test_reverse_url_resolves_to_password_reset_done_view(self):
        found = resolve(reverse("accounts:password-reset-done"))
        self.assertEqual(found.func, password_reset_done)

    def test_reverse_url_resolves_to_password_reset_complete_view(self):
        found = resolve(reverse("accounts:password-reset-complete"))
        self.assertEqual(found.func, password_reset_complete)

