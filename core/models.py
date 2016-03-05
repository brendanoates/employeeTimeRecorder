from django.db import models


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self upddating "created" and "modified" fields.
    """
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class NamedModel(TimeStampedModel):
    """
    An abstract base class TimeStampedModel that provides a "name" field.
    """
    name = models.CharField(max_length=100)

    class Meta:
        abstract = True