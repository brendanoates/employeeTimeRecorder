from django.core.urlresolvers import reverse
from django.test import Client, TestCase

from profiles.models import EmployeeTimeRecorderUser as User

'''
 Unit test the registration view, must be able to register with a unique user id or receive an error response if id
 is not unique
'''


class ProfileViewTest(TestCase):
    """
    # create a user to test the profile view
    """

    def setUp(self):
        self.USERNAME = 'testuser'
        self.PASSWORD = 'testPassword'
        self.STAFFNUMBER = '12345'
        self.MANAGER_EMAIL = 'manager.name'
        client = Client()
        client.post(reverse('accounts:accounts-register'),
                    {'username': self.USERNAME, 'password': self.PASSWORD})
        client.get(reverse('accounts:accounts-logout'))

    def __login(self):
        client = Client()
        client.post(reverse('accounts:accounts-login'), {'username': self.USERNAME, 'password': self.PASSWORD})
        return client

    def test_profile_page_contains_correct_html_(self):
        client = self.__login()
        response = client.get(reverse('profiles:profiles'))
        self.assertTrue(response.content.startswith(b'<!doctype html>'))
        self.assertIn(b'<title>Profile</title>', response.content)
        self.assertIn(b'<label for="id_staff_number">Staff Number:</label>', response.content)
        self.assertTrue(response.content.endswith(b'</html>'))
        client.get(reverse('accounts:accounts-logout'))

    def test_profile_allows_update(self):
        client = self.__login()
        user = User.objects.get(username=self.USERNAME)
        self.assertNotEqual(user.staff_number, self.STAFFNUMBER)
        self.assertNotEqual(user.manager_email, self.MANAGER_EMAIL)
        response = client.post(reverse('profiles:profiles'),
                               {'staff_number': self.STAFFNUMBER, 'manager_email': self.MANAGER_EMAIL})
        self.assertContains(response, '', status_code=302)
        self.assertEqual(response.url, reverse('index'))  # should redirect to index
        client.get(reverse('accounts:accounts-logout'))
        user = User.objects.get(username=self.USERNAME)
        self.assertEqual(user.staff_number, self.STAFFNUMBER)
        self.assertEqual(user.manager_email, self.MANAGER_EMAIL)
