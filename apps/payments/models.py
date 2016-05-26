from django.db import models

from pupil.models import PupilTutorMatch, Pupil
from tutor.models import Tutor
from option.models import AvailableTutorSubject


class LessonRecord(models.Model):
    datetime = models.DateTimeField(auto_now=True, verbose_name='date/time')
    pupil = models.ForeignKey(Pupil, null=True)
    tutor = models.ForeignKey(Tutor, null=True)
    subject = models.ForeignKey(AvailableTutorSubject, null=True)
    amount = models.IntegerField(verbose_name='amount', null=True)
    paid_status = models.BooleanField(verbose_name='Paid', default=False)
    payment_record = models.ForeignKey('PaymentRecord', null=True, blank=True)
    # duration = models.DecimalField(max_digits=5, decimal_places=1, default=1)

    def __unicode__(self):
        return '%s: %s (%s %s) taught by %s - R%s' % (
            self.datetime.strftime('%d-%m-%Y %H:%M'),
            self.pupil,
            self.pupil.level_of_study,
            self.subject,
            self.tutor,
            self.amount,
        )

    def delete(self, *args, **kwargs):
        payment_record1 = PaymentRecord.objects.get(pk=self.payment_record.id)
        print 'payment record', payment_record1
        if not payment_record1.paid:
            payment_record1.amount -= self.amount
            payment_record1.save()
        super(LessonRecord, self).delete()


class PaymentRecord(models.Model):
    amount = models.IntegerField(verbose_name='amount', null=True)
    date = models.DateTimeField(auto_now=True, null=True)
    tutor = models.ForeignKey(Tutor, null=False, blank=False)
    paid = models.BooleanField(default=False)

    def __unicode__(self):
        return '%s %s - R%s Paid:%s' % (self.date.strftime('%d-%m-%Y %H:%M'),
                                        self.tutor, self.amount, self.paid)

    def save(self, *args, **kwargs):
        # if I change paid to true I want to hcange all its lesson records paid to be true too
        # if self.paid:
        lessons = LessonRecord.objects.filter(payment_record=self)
        for lesson in lessons:
            lesson.paid_status = self.paid
            lesson.save()
        super(PaymentRecord, self).save(*args, **kwargs)


class ProgressReport(models.Model):
    HOMEWORK_STATUS_CHOICE = (
        ('Complete', 'Complete'),
        ('Partially Complete', 'Partially Complete'),
        ('Not Complete', 'Not Complete'),
        ('First Lesson', 'First Lesson')
    )
    NUMBER_OF_HOURS = (
        (0.5, '30min'),
        (1, '1 hour'),
        (1.5, '1hour30min'),
        (2, '2 hours')
    )
    homework_status = models.CharField(max_length=20, choices=HOMEWORK_STATUS_CHOICE,
                                       verbose_name='Homework completed?')
    homework_summary = models.TextField(max_length=160, help_text="give a week's worth of HW (160 Characters)",
                                        verbose_name='Summary of homework given')
    student_summary = models.TextField(max_length=200,
                                       help_text='Indicate how student is coping with work, what needs '
                                                 'improving, tutor advice, etc',
                                       verbose_name='Summary of student progress')
    duration = models.DecimalField(max_digits=3, decimal_places=1, choices=NUMBER_OF_HOURS, default=1)
    lesson = models.OneToOneField(LessonRecord, null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.lesson


class TutorFee(models.Model):
    rate_category = models.CharField(unique=True, max_length=20)
    rate = models.IntegerField()

    def __unicode__(self):
        return '%s - R%s' % (self.rate_category, self.rate)
