from django.contrib import admin

from models import PendingPayment, LessonRecord, PaymentRecord

admin.site.register(PendingPayment)
admin.site.register(LessonRecord)
admin.site.register(PaymentRecord)
