from django.test import TestCase

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
        self.assertEqual(self.user.get_managers_email(), self.MANAGER_EMAIL + '@emailaddress.com')
