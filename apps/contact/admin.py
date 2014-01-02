from django.contrib import admin
from models import Contact

class ContactAdmin(admin.ModelAdmin):
    search_fields = [ "name", ]
    list_display =  ("name",)


admin.site.register(Contact, ContactAdmin)