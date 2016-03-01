from django.contrib.auth.models import AbstractUser
from django.db import models


class EmployeeTimeRecorderUser(AbstractUser):
    staff_number = models.CharField(max_length=10)
