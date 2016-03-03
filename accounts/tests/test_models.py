from importlib import import_module

from django.conf import settings
from django.core.urlresolvers import reverse, resolve
from django.http import HttpRequest
from django.test import Client, TestCase
from accounts.views import register as registration_page
from profiles.models import EmployeeTimeRecorderUser as User

'''
 Unit test the EmployeeTimeRecorderUser model
'''
class EmployeeTimeRecorderUserTest(TestCase):
    STAFFNUMBER = '12345'
    MANAGER_EMAIL = 'manager.nae'
    user = None

    def setUp(self):
        self.user = User.objects.create_user(username='testuser')
    def test_get_managers_email(self):
        self.assertEqual(self.user.get_managers_email(), None)
        self.user.manager_email = self.MANAGER_EMAIL
        self.assertEqual(self.user.get_managers_email(), self.MANAGER_EMAIL+'@amadeus.com')
