from django.contrib.auth import get_user_model
from django.test import TestCase

from claims.forms import NewClaimForm
from claims.models import ClaimType
from profiles.models import EmployeeTimeRecorderUser
from tests.functional_tests.test_task_stories import populate_database


class ClientFormTest(TestCase):

    def setUp(self):
        populate_database()
        self.user = get_user_model().objects.create_user('testuser')
        self.manager = EmployeeTimeRecorderUser.objects.get(username='Manager1')

        self.claim_type1 = ClaimType(name='type1', count=False)

    def test_valid_data(self):
        form = NewClaimForm(
            {'authorising_manager': 3,
            'type': 1,
            'claim_value': "1",
            'date': '28 March 2016'
        })
        self.assertTrue(form.is_valid())

    def test_invalid_data1(self):
        form = NewClaimForm(
            {'authorising_manager': 3,
            'type': 8,
            'claim_value': "1.5",
            'date': '28 March 2016'
        })
        self.assertFalse(form.is_valid())

    def test_invalid_data2(self):
        form = NewClaimForm(
            {'authorising_manager': 3,
            'type': 11,
            'claim_value': "1.5",
            'date': '28 March 2016'
        })
        self.assertFalse(form.is_valid())


