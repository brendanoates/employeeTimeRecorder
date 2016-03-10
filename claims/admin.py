from django.contrib import admin

from claims.models import Claim, ClaimType

# Register your models here.
admin.site.register(Claim)
admin.site.register(ClaimType)
