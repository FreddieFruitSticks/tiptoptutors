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
        return '%s: %s (%s) taught by %s - R%s' % (
            self.datetime.strftime('%d-%m-%Y %H:%M'),
            self.pupiltutormatch.pupil,
            self.pupiltutormatch.subject,
            self.pupiltutormatch.tutor,
            self.amount
        )


class PaymentRecord(models.Model):
    tutor = models.ForeignKey(Tutor)
    amount_paid = models.IntegerField(verbose_name='amount paid')

    def __unicode__(self):
        return '%s - R%s' % (self.tutor, self.amount_paid)


class ProgressReport(models.Model):
    HOMEWORK_STATUS_CHOICE = (
        ('Complete', 'Complete'),
        ('Partially Complete', 'Partially Complete'),
        ('Not Complete', 'Not Complete'),
        ('First Lesson', 'First Lesson')
    )
    homework_status = models.CharField(max_length=20, choices=HOMEWORK_STATUS_CHOICE)
    homework_given = models.BooleanField(help_text='select if homework was given')
    homework_summary = models.TextField(max_length=160, help_text="give a week's worth of HW (160 Characters)",
                                        verbose_name='Summary of homework given')

    student_summary = models.TextField(max_length=200,
                                       help_text='Indicate how student is coping with work, what needs '
                                                 'improving, tutor advice, etc',
                                       verbose_name='Summary of student progress')
