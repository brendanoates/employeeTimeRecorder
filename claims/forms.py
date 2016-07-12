from datetime import datetime

from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ModelForm
from django.utils.html import format_html
from django.utils.safestring import mark_safe

from claims import logger
from claims.models import Claim, ClaimType
from profiles.models import EmployeeTimeRecorderUser

class ClaimForm(ModelForm):

    class Meta:
        model = Claim
        exclude = ['owner', 'processed', 'senior_manager', 'authorised', 'senior_authorised']
        fields =('date','claim_value')

        widgets = {
            'date': DateTimePicker(options={"format": "DD MMMM YYYY", "pickTime": False,
                                                    "defaultDate": datetime.now().strftime("%d %B %Y")})
        }
        help_texts = {
            'date': 'Please enter the date the claim applies to',
            'claim_value': 'Please enter the value of the claim',
        }

    def __init__(self, *args, **kwargs):
        self.claim_id = kwargs.pop('claim_id', None)
        super(ClaimForm, self).__init__(*args, **kwargs)
        self.fields['authorising_manager'] = forms.ModelChoiceField(queryset=EmployeeTimeRecorderUser.objects.
                                                 filter(groups__permissions__name="Can authorise claim").
                                                 order_by('username'),
                                                 label='Authorising Manager',
                                                 help_text='Please select the manager to authorise your claim',
                                                 required=True)
        self.fields['type'] = forms.ModelChoiceField(queryset=ClaimType.objects.all().order_by('name'),
                                                     label='Type of claim',
                                                     help_text='Please select the claim type that you want to create',
                                                     required=True)
        # self.fields[''] = forms.FloatField(label='Value',
        #                                               help_text=,
        #                                               required=True)
        # self.fields['date'] = forms.DateField(required=False,input_formats=['%d %B %Y'],
        #                                       help_text=,
        #                                       )


    def clean_claim_value(self):
        try:
            claim_type = ClaimType.objects.get(pk=self.data['type'])
            claim_value = float(self.data['claim_value'])
            if claim_type.count and not claim_value.is_integer():
                raise forms.ValidationError('You have not entered a valid value, it should be a whole number for this '
                                            'type of claim')
            if claim_type.maximum_value < float(claim_value):
                raise forms.ValidationError('The value you are trying to claim exceeds the maximum allowed for this '
                                            'type of claim')
            return claim_value
        except forms.ValidationError:
            raise
        except:
            logger.exception('Exception:')
            raise forms.ValidationError('An error occured durring the validation, please try again')


class UpdateClaimForm(ClaimForm):

    def clean_type(self):
        claim_type = self.cleaned_data['type']
        date_object = self.cleaned_data['date']
        if not claim_type.allow_multiple and Claim.objects.filter(type=claim_type, date=date_object,).\
                exclude(id__in=[self.claim_id]).exists():
            raise forms.ValidationError('You have already made a claim for this type on this date')
        return claim_type

class NewClaimForm(ClaimForm):
    def clean_type(self):
        claim_type = self.cleaned_data['type']
        date_object = self.cleaned_data['date']
    #         self.cleandate = date_object
    #     except:
    #         # self.data['date'] = ''
    #         raise forms.ValidationError('The date is not valid, eg 01 January 2016 or try using the date picker')
        if not claim_type.allow_multiple and Claim.objects.filter(type=claim_type, date=date_object).exists():
            raise forms.ValidationError('You have already made a claim for this type on this date')
        return claim_type



class FilterClaimForm(forms.Form):
    authorised = forms.BooleanField(help_text='select if you only want authorised claims')
    date_after = forms.DateField(required=False, input_formats=('%d %B %Y',), help_text="view claims after this date",
                                 widget=DateTimePicker(options={"format": "DD MMMM YYYY", "size": 12}))
    date_before = forms.DateField(required=False, input_formats=('%d %B %Y',), help_text="view claims before this date",
                                  widget=DateTimePicker(options={"format": "DD MMMM YYYY", "size": 12}))
    type = forms.ModelChoiceField(queryset=ClaimType.objects.all().order_by('name'), label='Type of claim',
                                  help_text='Show only claims of selected type')

class FilterAuthoriseClaimForm(forms.Form):
    other_manager = forms.ModelChoiceField(queryset=EmployeeTimeRecorderUser.objects.
                                                 filter(groups__permissions__name="Can authorise claim").
                                                 order_by('username'),
                                           label='Authorising Manager',
                                           help_text='If you want to authorise claims for another manager please '
                                                     'select their id',
                                           required=False)
