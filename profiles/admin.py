from django.contrib import admin

from profiles.models import EmployeeTimeRecorderUser


# Register your models here.


class EmployeeTimeRecorderUserAdmin(admin.ModelAdmin):
    filter_horizontal = ('groups', 'user_permissions')
    normaluser_fields = ['groups',]

    def get_form(self, request, obj=None, **kwargs):
        if not request.user.is_superuser:
            self.fields = self.normaluser_fields

        return super(EmployeeTimeRecorderUserAdmin, self).get_form(request, obj, **kwargs)

admin.site.register(EmployeeTimeRecorderUser, EmployeeTimeRecorderUserAdmin)
