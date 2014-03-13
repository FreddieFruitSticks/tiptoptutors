from django.contrib import admin

from matchmaker import models


class PupilMatchingAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.PupilProxy, PupilMatchingAdmin)