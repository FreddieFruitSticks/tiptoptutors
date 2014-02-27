from django.contrib import admin
from models import Tutor

class TutorAdmin(admin.ModelAdmin):
    search_fields = [ "name", 'surname', 'mobile', 'email', 'subject' ]
    list_display  =  ("name", 'surname', 'mobile', 'email', )
    list_filter   = ('subject',)

    fieldsets = (
        ('Admin', {
            'fields': ('student', 'lesson', 'comment')
        }),

        ('Tutor details', {
            'fields': ('name', 'surname', 'mobile', 'email', 'subject', 'cv', 'academic')
        }),
    )

admin.site.register(Tutor, TutorAdmin)
