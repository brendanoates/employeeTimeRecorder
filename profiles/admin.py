from django.contrib import admin

from profiles.models import EmployeeTimeRecorderUser


# Register your models here.


class EmployeeTimeRecorderUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')

admin.site.register(EmployeeTimeRecorderUser, EmployeeTimeRecorderUserAdmin)