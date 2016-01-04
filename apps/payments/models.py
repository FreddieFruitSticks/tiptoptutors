from django.db import models

from pupil.models import PupilTutorMatch
from tutor.models import Tutor


class PendingPayment(models.Model):
    tutor = models.ForeignKey(Tutor, unique=True)
    amount_owing = models.IntegerField(null=True, blank=True, verbose_name="amount owing")

    def __unicode__(self):
        return '%s - R%s' % (self.tutor, self.amount_owing)


class LessonRecord(models.Model):
    datetime = models.DateTimeField(auto_now=True, verbose_name='date/time')
    pupiltutormatch = models.ForeignKey(PupilTutorMatch)
    amount = models.IntegerField(verbose_name='amount')

    def __unicode__(self):
        return '%s: %s (%s) - R%s' % (
            self.datetime.strftime('%d-%m-%Y %H:%M'),
            self.pupiltutormatch.pupil,
            self.pupiltutormatch.subject,
            self.amount
        )


class PaymentRecord(models.Model):
    tutor = models.ForeignKey(Tutor)
    amount_paid = models.IntegerField(verbose_name='amount paid')

    def __unicode__(self):
        return '%s - R%s' % (self.tutor, self.amount_paid)
