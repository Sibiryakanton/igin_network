from django.contrib import admin
from . import models


class CountryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(models.Country, CountryAdmin)
admin.site.register(models.ProfileModel)
