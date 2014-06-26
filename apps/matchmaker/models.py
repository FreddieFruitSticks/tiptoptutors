import random
import re

from django.db import models
from django.db.models import Count, F, Q
from django.dispatch import receiver
from django.utils import timezone

from option.models import AvailableTutorSubject
from pupil.models import Pupil, PupilTutorMatch
from sms.models import SMS
from sms.api import sms_reply_received
from tutor.models import Tutor


# numbers + lowercase + uppercase
REQUEST_CODE_CHARSET = [chr(i) for i in range(ord('0'), ord('9') + 1)] + \
                       [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
                       [chr(i) for i in range(ord('A'), ord('Z') + 1)]

# Change with care. These WHERE clauses should work on MySQL, SQLite and Postgres.
WHERE_PUPILS_WITH_UNMATCHED_SUBJECTS = (
    "NOT EXISTS (SELECT * FROM pupil_pupiltutormatch "
    "WHERE pupil_pupiltutormatch.pupil_id = pupil_pupil.id AND "
    "option_availabletutorsubject.id = pupil_pupiltutormatch.subject_id AND "
    "pupil_pupiltutormatch.start_date <= %s AND (pupil_pupiltutormatch.end_date "
    "IS NULL OR pupil_pupiltutormatch.end_date >= %s))"
)
WHERE_PUPILS_WITHOUT_UNMATCHED_SUBJECTS = (
    "NOT EXISTS (SELECT pupil_pupil_subject.availabletutorsubject_id FROM "
    "pupil_pupil_subject WHERE pupil_pupil_subject.pupil_id = pupil_pupil.id "
    "AND NOT EXISTS (SELECT * FROM pupil_pupiltutormatch WHERE "
    "pupil_pupiltutormatch.subject_id = pupil_pupil_subject.availabletutorsubject_id "
    "AND pupil_pupiltutormatch.pupil_id = pupil_pupil.id AND pupil_pupiltutormatch.start_date "
    "<= %s AND (pupil_pupiltutormatch.end_date IS NULL OR pupil_pupiltutormatch.end_date >= %s)))"
)


class PupilQuerySet(models.query.QuerySet):

    def some_unmatched(self):
        date_now = timezone.now().date()
        return self.extra(tables=['option_availabletutorsubject'],
                          where=[WHERE_PUPILS_WITH_UNMATCHED_SUBJECTS],
                          params=[date_now, date_now]).distinct()

    def all_matched(self):
        date_now = timezone.now().date()
        return self.extra(where=[WHERE_PUPILS_WITHOUT_UNMATCHED_SUBJECTS],
                          params=[date_now, date_now])


class PupilManager(models.Manager):

    def get_queryset(self):
        return PupilQuerySet(self.model, using=self._db)

    def some_unmatched(self):
        return self.get_queryset().some_unmatched()

    def all_matched(self):
        return self.get_queryset().all_matched()


class PupilProxy(Pupil):
    objects = PupilManager()

    class Meta:
        proxy = True
        verbose_name = 'pupil'
        verbose_name_plural = 'pupils'
        ordering = ('-created_at', 'surname', 'name')

    def __unicode__(self):
        return '%s: %s for %s (%s)' % (
            self.created_at.strftime('%d-%m-%Y %H:%M'),
            self.name,
            ', '.join(s.name for s in self.unmatched_subjects),
            self.level_of_study
        )

    @property
    def needs_tutor(self):
        return self.unmatched_subjects.exists()

    @property
    def unmatched_subjects(self):
        date_now = timezone.now().date()
        # get subjects actively being tutored
        matched_subject_ids = list(PupilTutorMatch.objects.filter(
            Q(end_date__isnull=True)|Q(end_date__gte=date_now),
            pupil=self,
            start_date__lte=date_now).values_list('subject_id', flat=True))
        return self.subject.exclude(id__in=matched_subject_ids)


class TutorProxy(Tutor):

    class Meta:
        proxy = True
        verbose_name = 'available tutor'
        verbose_name_plural = 'available tutors'

    def __unicode__(self):
        return '%s %s' % (self.name, self.surname)

    @property
    def subject_str(self):
        return ', '.join(self.subject.values_list('name', flat=True))

    def matching_subjects(self, subject_ids):
        return self.subject.filter(id__in=subject_ids)


class RequestForTutor(models.Model):
    '''
    This is the base class for tutor requests. In future, multiple
    communication media might be used to reach out to tutors. Only
    generic functionality should go here.
    '''
    pupil = models.ForeignKey(PupilProxy)
    subject = models.ForeignKey(AvailableTutorSubject)
    # active: initial state, tutors can apply for this matchup
    # inactive: probably after a tutor has been selected, applications
    # will be ignored
    status = models.CharField(
        max_length=8,
        default='active',
        choices=(('active', 'Active'),
                 ('inactive', 'Inactive'))
    )
    code = models.CharField(unique=True, max_length=12)
    created = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def generate_unique_code(length=6, charset=REQUEST_CODE_CHARSET):
        code = None
        while not code:
            code = ''.join(random.choice(charset) for i in range(length))
            if RequestForTutor.objects.filter(code=code).exists():
                code = None
        return code

    def save(self, *args, **kwargs):
        if not self.pk and not self.code:
            self.code = self.generate_unique_code()
        super(RequestForTutor, self).save(*args, **kwargs)


class RequestSMS(SMS):

    class Meta:
        verbose_name = 'Request SMS'
        verbose_name_plural = "Request SMSes"

    requests = models.ManyToManyField(RequestForTutor)
    tutor = models.ForeignKey(TutorProxy)
    response_text = models.CharField(max_length=32, null=True, blank=True)
    response_timestamp = models.DateTimeField(null=True, blank=True)

    @property
    def codes(self):
        if not self.response_text:
            return []
        return [c[0].strip() for c in
                re.findall(r'(\w{6,12}($|\s+))',
                           self.response_text,
                           re.DOTALL)]


@receiver(sms_reply_received)
def save_requestsms_response(sender, **kwargs):
    try:
        sms_obj = RequestSMS.objects.get(pk=kwargs['instance'].pk)
        sms_obj.response_text = kwargs['text']
        sms_obj.response_timestamp = kwargs['timestamp']
        sms_obj.save()
    except RequestSMS.DoesNotExist:
        pass
