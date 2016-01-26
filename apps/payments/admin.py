from django.contrib import admin

from models import LessonRecord, PaymentRecord, ProgressReport, TutorFee


# class PendingPayments(admin.AdminSite):


admin.site.register(LessonRecord)
admin.site.register(PaymentRecord)
admin.site.register(ProgressReport)
admin.site.register(TutorFee)
