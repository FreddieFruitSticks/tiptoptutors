from django.contrib import admin
from models import Student


class StudentAdmin(admin.ModelAdmin):
<<<<<<< HEAD
    search_fields = [ "name", "email" ]
    list_display =  ("name","email")
=======
    search_fields = [ "name", 'surname', 'email',  ]
    list_display =  ("name", 'surname', 'email', 'contact_number',)
>>>>>>> a3dc19d0d9280e9a8ba7cc9608263dd05a4804ef


admin.site.register(Student, StudentAdmin)