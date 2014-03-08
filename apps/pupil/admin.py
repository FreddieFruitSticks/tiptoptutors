from django.contrib import admin
from models import Pupil


class PupilAdmin(admin.ModelAdmin):

    search_fields = [ "name", 'surname', 'email',  ]
    list_display =  ("name", 'surname', 'email', 'contact_number','created_at')



admin.site.register(Pupil, PupilAdmin)