from django.contrib import admin

from models import PendingPayment, LessonRecord, PaymentRecord, ProgressReport


# class PendingPayments(admin.AdminSite):


admin.site.register(PendingPayment)
admin.site.register(LessonRecord)
admin.site.register(PaymentRecord)
admin.site.register(ProgressReport)
