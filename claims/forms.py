from datetime import datetime

from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from claims.models import Claim, ClaimType
from profiles.models import EmployeeTimeRecorderUser


class ClaimForm(ModelForm):
    authorising_manager = forms.ModelChoiceField(queryset=EmployeeTimeRecorderUser.objects.
                                                 filter(groups__permissions__name="Can authorise claim").
                                                 order_by('username'),

                                                 label='Authorising Manager',
                                                 help_text='Please select the manager to authorise your claim',
                                                 required=True)

    type = forms.ModelChoiceField(queryset=ClaimType.objects.all().order_by('name'), label='Type of claim',
                                  help_text='Please select the claim type that you want to create', required=True)
    claim_value = forms.FloatField(label='Value', help_text='Please enter the claim_value of the claim ', required=True)
    date = forms.DateField(required=False, input_formats=('%d %B %Y',), help_text="Please enter the date the claim "
                                                                                  "applies to",
                           widget=DateTimePicker(options={"format": "DD MMMM YYYY", "size": 12}))

    def clean(self):
        cleaned_data = super(ClaimForm, self).clean()
        type = cleaned_data.get('type')
        claim_value = cleaned_data.get('claim_value')
        date = self.data.get('date')
        authorising_manager = self.data.get('authorising_manager')
        if type and type.count and not claim_value.is_integer():
            raise forms.ValidationError('You have not entered a valid count value, it should be a whole number')
        if type and claim_value and type.maximum_value < claim_value:
            raise forms.ValidationError('The value you are trying to claim exceeds the maximum allowed for the claim '
                                        'type')
        try:
            date_object = datetime.strptime(date, '%d %B %Y')
            self.date = date_object
        except:
            self.data['date'] = ''
            raise forms.ValidationError('The date is not valid, eg 01 January 2016 or try using the date picker')
        if type and not type.allow_multiple and Claim.objects.filter(date=date_object, type=type,
                                                                     authorising_manager=authorising_manager):
            raise forms.ValidationError('You have already made a claim for this type on this date')

    class Meta:
        model = Claim
        exclude = ['owner', 'processed', 'senior_manager', 'authorised', 'senior_authorised']


class FilterClaimForm(forms.Form):
    authorised = forms.BooleanField(help_text='select if you only want authorised claims')
    date_after = forms.DateField(required=False, input_formats=('%d %B %Y',), help_text="view claims after this date",
                                 widget=DateTimePicker(options={"format": "DD MMMM YYYY", "size": 12}))
    date_before = forms.DateField(required=False, input_formats=('%d %B %Y',), help_text="view claims before this date",
                                  widget=DateTimePicker(options={"format": "DD MMMM YYYY", "size": 12}))
    type = forms.ModelChoiceField(queryset=ClaimType.objects.all().order_by('name'), label='Type of claim',
                                  help_text='Show only claims of selected type')