from django.contrib import admin
from models import Student


class StudentAdmin(admin.ModelAdmin):
    search_fields = [ "name", "email" ]
    list_display =  ("name","email")


admin.site.register(Student, StudentAdmin)