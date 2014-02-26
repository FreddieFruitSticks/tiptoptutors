from django.contrib import admin
from models import Tutor

class TutorAdmin(admin.ModelAdmin):
    search_fields = [ "name", ]
    list_display =  ("name",)


admin.site.register(Tutor, TutorAdmin)
