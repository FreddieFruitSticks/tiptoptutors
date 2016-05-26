from django.db.models.signals import pre_save
from django.dispatch import receiver
from payments.models import PaymentRecord

__author__ = 'freddie'


@receiver(pre_save, sender=PaymentRecord)
def update_Lessons_records(sender, **kwargs):
    print sender
    print kwargs
    print 'inside update lessons receiver'
