from django.core.urlresolvers import reverse, resolve

from django.test import Client, TestCase

from profiles.views import profile as profile_page



class PageTests(TestCase):

    def test_reverse_url_resolves_to_profile_page_view(self):
        found = resolve(reverse("profiles:profiles"))
        self.assertEqual(found.func, profile_page)


