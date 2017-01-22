from django.db.models.signals import pre_save, pre_delete, post_init, post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives, BadHeaderError

from payments.models import PaymentRecord, LessonRecord
from pupil.models import Pupil
from tutor.models import Tutor

__author__ = 'freddie'


@receiver(pre_save, sender=PaymentRecord)
def update_lessons_records(sender, **kwargs):
    payment_record = kwargs.get('instance')
    lessons = LessonRecord.objects.filter(payment_record=payment_record)
    for lesson in lessons:
        if lesson.paid_status != payment_record.paid:
            lesson.paid_status = payment_record.paid
            lesson.save()


@receiver(pre_delete, sender=LessonRecord)
def update_payment_record(sender, **kwargs):
    lesson_record = kwargs.get('instance')
    payment_record1 = PaymentRecord.objects.get(pk=lesson_record.payment_record.id)
    if not payment_record1.paid:
        payment_record1.amount -= lesson_record.amount
        payment_record1.save()


@receiver(post_save,sender=Pupil)
def send_new_pupil_admin_email(sender, **kwargs):
    pupil = kwargs.get('instance')
    try:
        mesg = EmailMultiAlternatives('New Pupil', '', 'info@tiptoptutors.co.za',
                                      ['freddieodonnell@gmail.com'])
        mesg.attach_alternative('NEW PUPIL REGISTERED: '+ pupil.name, 'text/html')
        mesg.send()
        print 'sent'
    except BadHeaderError:
        pass


@receiver(post_save,sender=Tutor)
def send_new_tutor_admin_email(sender, **kwargs):
    tutor = kwargs.get('instance')
    try:
        mesg = EmailMultiAlternatives('New Tutor', '', 'info@tiptoptutors.co.za',
                                      ['info@tiptoptutors.co.za'])
        mesg.attach_alternative('NEW TUTOR REGISTERED: '+ tutor.name, 'text/html')
        mesg.send()
    except BadHeaderError:
        pass
