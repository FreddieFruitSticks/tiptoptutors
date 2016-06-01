from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver

from payments.models import PaymentRecord, LessonRecord

__author__ = 'freddie'


@receiver(pre_save, sender=PaymentRecord)
def update_lessons_records(sender, **kwargs):
    payment_record = kwargs.get('instance')
    lessons = LessonRecord.objects.filter(payment_record=payment_record)
    for lesson in lessons:
        lesson.paid_status = payment_record.paid
        lesson.save()


@receiver(pre_delete, sender=LessonRecord)
def update_payment_record(sender, **kwargs):
    lesson_record = kwargs.get('instance')
    payment_record1 = PaymentRecord.objects.get(pk=lesson_record.payment_record.id)
    if not payment_record1.paid:
        payment_record1.amount -= lesson_record.amount
        payment_record1.save()
