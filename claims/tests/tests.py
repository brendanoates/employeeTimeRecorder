from django.core.urlresolvers import reverse, resolve
from django.test import TestCase

from claims.views import new_claim


class PageTests(TestCase):
    def test_reverse_url_resolves_to_new_claim_view(self):
        found = resolve(reverse("claims:new_claim"))
        self.assertEqual(found.func, new_claim)
