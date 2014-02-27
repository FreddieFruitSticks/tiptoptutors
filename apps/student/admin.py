from django.contrib import admin
from models import Student


class StudentAdmin(admin.ModelAdmin):
    search_fields = [ "name", 'surname', 'email',  ]
    list_display =  ("name", 'surname', 'email', 'contact_number',)


admin.site.register(Student, StudentAdmin)