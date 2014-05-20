from django.contrib import admin
from quote.models import Quote

class QuoteAdmin(admin.ModelAdmin):
    search_fields = [ "name", "email"]
    list_display =  ("name", "email")


admin.site.register(Quote, QuoteAdmin)
