from django.contrib.auth import get_user_model
from django.test import TestCase

from claims.forms import ClaimForm
from claims.models import ClaimType


class ClientFormTest(TestCase):

    def setUp(self):
        user = get_user_model().objects.create_user('testuser')
        self.claim_type1 = ClaimType(name='type1', count=False)

    def test_init(self):
        ClaimForm(type=self.claim_type1)

    def test_init_without_entry(self):
        with self.assertRaises(KeyError):
            ClaimForm()

    def test_valid_data(self):
        form = ClaimForm({
            'name': "Turanga Leela",
            'email': "leela@example.com",
            'body': "Hi there",
        }, entry=self.entry)
        self.assertTrue(form.is_valid())
        comment = form.save()
        self.assertEqual(comment.name, "Turanga Leela")
        self.assertEqual(comment.email, "leela@example.com")
        self.assertEqual(comment.body, "Hi there")
        self.assertEqual(comment.entry, self.entry)

def test_blank_data(self):
    form = ClaimForm({}, entry=self.entry)
    self.assertFalse(form.is_valid())
    self.assertEqual(form.errors, {
        'name': ['required'],
        'email': ['required'],
        'body': ['required'],
    })