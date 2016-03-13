from django.conf import settings
from django.db import models

from core.models import TimeStampedModel, NamedModel


class ClaimTypeManager(models.Manager):
    def create_claim_type(self, name, count):
        claim_type = ClaimType(name=name, count=count)
        return claim_type


class ClaimType(NamedModel):
    """
    A class that defines a claim type it will either applies a "count" of the number of occurrences for the claim OR the
    number of "hours"
    """
    count = models.BooleanField(help_text='Selct this field if the value held for this claim type is a count of or '
                                          'number of occurances as opposed to the number of hours')
    allow_multiple = models.BooleanField(default=False, help_text='Select this field if more than one claim of this '
                                                                  'type can exist for a particular date')
    maximum_value = models.FloatField(default=1, help_text='The maximum value a claim of this type can hold i.e for a '
                                                           'shift it would 1 and for an hours it would be 24')

    objects = ClaimTypeManager()

    def is_count(self):
        return self.count

    def is_hours(self):
        return not self.count

    def __str__(self):
        return self.name


class Claim(TimeStampedModel):
    """
    A class that defines a claim it dependant on the type the value
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='related owner', related_name='claim_owner')
    authorising_manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='authorising manager', null=True,
                                            blank=True, related_name='claim_authorising_manager')
    senior_manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='senior manager', null=True,
                                       blank=True, related_name='claim_senior_manager')
    type = models.ForeignKey(ClaimType, verbose_name='related type')
    date = models.DateTimeField()
    value = models.FloatField()
    authorised = models.BooleanField(db_index=True, default=False)
    senior_authorised = models.BooleanField(db_index=True, default=False)
    processed = models.BooleanField(db_index=True, default=False)

    def __str__(self):
        return ', '.join([self.owner.get_username(), str(self.date), str(self.type), ('value: ' + str(self.value))])
