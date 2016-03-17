'''
 Unit test the claims views
'''
from django.contrib.auth.models import AnonymousUser
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from claims.views import new_claim
from profiles.models import EmployeeTimeRecorderUser as User

class SimpleTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@…', password='top_secret')

    def test_new_claim(self):
        # Create an instance of a GET request.
        request = self.factory.get(reverse('claims:new_claim'))
        # simulate a logged-in user by setting request.user manually.
        request.user = self.user
        # Test new_claim() as if it were deployed at /claims/new_claim
        response = new_claim(request)
        self.assertEqual(response.status_code, 200)
        # Create an instance of a POST request.
        request = self.factory.post(reverse('claims:new_claim'), {'authorising_maager': ['1'], 'date': ['21 March 2016'],
                                                                  'type': ['1'], 'claim_value': ['1']})
        response = new_claim(request)
        self.assertEqual(response.status_code, 200)