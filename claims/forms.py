from datetime import datetime

from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.forms import ModelForm

from claims.models import Claim, ClaimType


class ClaimForm(ModelForm):
    type = forms.ModelChoiceField(queryset=ClaimType.objects.all().order_by('name'), label='Type of claim',
                                  help_text='Please select the claim type that you want to create', required=True)
    value = forms.FloatField(label='Value', help_text='Please enter the value of the claim ', required=True)
    date = forms.DateField(required=False, input_formats=('%d %B %Y',), help_text="Please enter the date the claim "
                                                                                  "applies to",
                           widget=DateTimePicker(options={"format": "DD MMMM YYYY", "size": 12} ))

    def clean(self):
        cleaned_data = super(ClaimForm, self).clean()
        type = cleaned_data.get('type')
        value = cleaned_data.get('value')
        date = self.data.get('date')
        if type and type.count and not value.is_integer():
            raise forms.ValidationError('You have not entered a valid count value')
        if type and value and type.maximum_value < value:
            raise forms.ValidationError('The value you are trying to claim exceeds the maximum allowed for the claim '
                                        'type')
        try:
            date_object = datetime.strptime(date, '%d %B %Y')
            self.date = date_object
        except:
            raise forms.ValidationError('The date is not valid')
        if type and not type.allow_multiple and Claim.objects.filter(date=date_object, type=type):
            raise forms.ValidationError('You have already made a claim for of this type on this date')
    class Meta:
        model = Claim
        exclude = ['owner', 'processed']


        # owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='related owner', related_name='claim_owner')
        #     authorising_manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='authorising manager', null=True,
        #                                             blank=True, related_name='claim_authorising_manager')
        #     senior_manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='senior manager', null=True,
        #                                        blank=True, related_name='claim_senior_manager')
        #     type = models.ForeignKey(ClaimType, verbose_name='related type')
        #     date = models.DateTimeField()
        #     value = models.FloatField()
        #
        #     processed = models.BooleanField(db_index=True)
