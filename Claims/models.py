from django.conf import settings
from django.db import models
from core.models import TimeStampedModel, NamedModel


class ClaimTypeManager(models.Manager):
    def create_claim_type(self, name, count):
        claim_type = ClaimType(name=name, count=count)
        return claim_type

class ClaimType(NamedModel):
    """
    A class that defines a claim type it will either applies a "count" of the number of occurances for the claim OR the
    number of "hours"
    """
    count = models.BooleanField()
    allow_multiple = models.BooleanField(default=False)

    objects = ClaimTypeManager()

    def is_count(self):
        return self.count

    def is_hours(self):
        return not self.count

    def __str__(self):
        return self.name + (' type: count' if self.count else ' type: hours')

class Claim(TimeStampedModel):
    """
    A class that defines a claim it dependant on the type the value
    """
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='related owner', related_name='claim_owner')
    type = models.ForeignKey(ClaimType, verbose_name='related type')
    date = models.DateTimeField()
    value = models.FloatField()
    authorising_manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='authorising manager', null=True,
                                            blank=True, related_name='claim_authorising_manager')
    senior_manager = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='senior manager', null=True,
                                            blank=True, related_name='claim_senior_manager')
    processed = models.BooleanField(db_index=True)

    def __str__(self):
        return ', '.join([self.owner.get_username(), str(self.date), str(self.type), ('value: ' + str(self.value))])
