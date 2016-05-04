from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from models import LessonRecord, PaymentRecord, ProgressReport, TutorFee
import models


class PaymentFilter(SimpleListFilter):
    title = 'paid status'
    parameter_name = 'has_been_paid'

    def lookups(self, request, model_admin):
        return (('1', 'Paid'),
                ('0', 'Unpaid'))

    def queryset(self, request, queryset):
        if self.value() == '1':
            return queryset.filter(paid=True)
        elif self.value() == '0':
            return queryset.filter(paid=False)


class PaymentsAdmin(admin.ModelAdmin):
    list_filter = [PaymentFilter]


admin.site.register(LessonRecord)
admin.site.register(PaymentRecord, PaymentsAdmin)
admin.site.register(ProgressReport)
admin.site.register(TutorFee)
