from django.contrib.auth.models import AbstractUser
from django.db import models


class EmployeeTimeRecorderUser(AbstractUser):
    staff_number = models.CharField(max_length=10, null=True, blank=True, default='')
    manager_email = models.CharField(max_length=30, null=True, blank=True, default='')

    def get_managers_email(self):
        ret_val = None
        if self.manager_email:
            ret_val = self.manager_email + '@amadeus.com'
        return ret_val
