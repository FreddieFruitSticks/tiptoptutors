from django.contrib import admin
from models import Student


class StudentAdmin(admin.ModelAdmin):
    search_fields = [ "name", ]
    list_display =  ("name",)


admin.site.register(Student, StudentAdmin)