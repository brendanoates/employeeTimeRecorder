from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

from claims.views import new_claim, view_claims, view_claim, authorisation_claims


class PageTests(TestCase):
    def test_reverse_url_resolves_to_new_claim_view(self):
        found = resolve(reverse("claims:new_claim"))
        self.assertEqual(found.func, new_claim)

    def test_reverse_url_resolves_to_view_claims_view(self):
        found = resolve(reverse("claims:view_claims"))
        self.assertEqual(found.func, view_claims)

    def test_reverse_url_resolves_to_view_claim_view(self):
        found = resolve(reverse("claims:view_claim", args=(1,)))
        self.assertEqual(found.func, view_claim)

    def test_reverse_url_resolves_to_authorisation_claims_view(self):
        found = resolve(reverse("claims:authorisation_claims"))
        self.assertEqual(found.func, authorisation_claims)
