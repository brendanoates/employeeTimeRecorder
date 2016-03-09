from __future__ import unicode_literals

from django import forms
from django.contrib.auth.forms import AuthenticationForm


class RegistrationForm(AuthenticationForm):
    staff_number = forms.CharField(max_length=10)
