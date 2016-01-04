import random
import re

from django.db import models
from django.db.models import Q

from django.dispatch import receiver

from option.models import AvailableTutorSubject
from pupil.models import Pupil, PupilTutorMatch
from sms.models import SMS
from sms.api import sms_reply_received
from tutor.models import Tutor



# numbers + lowercase + uppercase
REQUEST_CODE_CHARSET = set([chr(i) for i in range(ord('0'), ord('9') + 1)] + \
                           [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
                           [chr(i) for i in range(ord('A'), ord('Z') + 1)])
# remove letters that are easily mistaken for one another
REQUEST_CODE_CHARSET.remove('I')
REQUEST_CODE_CHARSET.remove('l')
REQUEST_CODE_CHARSET = list(REQUEST_CODE_CHARSET)


def filter_multi_value_queryset_as_list(parentlist, childlist):
    for pair in childlist:
        if pair in parentlist:
            parentlist.remove(pair)
    return parentlist


def get_pupil_ids(list_of_tuples):
    pupil_ids = []
    for entry in list_of_tuples:
        pupil_ids.append(entry[0])
    return pupil_ids


class PupilQuerySet(models.query.QuerySet):
    class Meta:
        app_label = 'matchmaker'

    def some_unmatched(self):
        list1 = list(PupilSubjectMatch.objects.values_list("pupil", "availabletutorsubject"))
        list2 = PupilTutorMatch.objects.values_list("pupil", "subject")
        pupil_ids = get_pupil_ids(filter_multi_value_queryset_as_list(list1, list2))
        return self.filter(id__in=pupil_ids).distinct()

    def all_matched(self):
        list1 = list(PupilSubjectMatch.objects.values_list("pupil", "availabletutorsubject"))
        list2 = PupilTutorMatch.objects.values_list("pupil", "subject")
        pupil_ids = get_pupil_ids(filter_multi_value_queryset_as_list(list1, list2))
        return self.exclude(id__in=pupil_ids).distinct()

    def actively_tutored(self):
        return self.paid().filter(id__in=PupilTutorMatch.objects.exclude(lessons_remaining=0).values_list('pupil'))

    def finished_lessons(self):
        print PupilTutorMatch.objects.filter(lessons_remaining=0).values_list('pupil')
        return self.filter(id__in=PupilTutorMatch.objects.filter(lessons_remaining=0).values_list('pupil'))

    def two_lessons_remaining(self):
        return self.paid().filter(
            id__in=PupilTutorMatch.objects.filter(Q(lessons_remaining=2) | Q(lessons_remaining=1)).values_list('pupil'))

    def unpaid(self):
        return self.filter(Q(id__in=PupilTutorMatch.objects.filter(Q(lessons_bought=None) | Q(lessons_bought=0))
                             .values('pupil')) | Q(pupiltutormatch__isnull=True)).distinct()

    def paid(self):
        return self.filter(id__in=PupilTutorMatch.objects.exclude(Q(lessons_bought=None) | Q(lessons_bought=0))
                           .values('pupil'))

    def get_all(self):
        return self.all()


class PupilManager(models.Manager):
    def get_queryset(self):
        return PupilQuerySet(self.model, using=self._db)

    def some_unmatched(self):
        return self.get_queryset().some_unmatched()

    def all_matched(self):
        return self.get_queryset().all_matched()

    def actively_tutored(self):
        return self.get_queryset().actively_tutored()

    def finished_lessons(self):
        return self.get_queryset().finished_lessons()

    def two_lessons_remaining(self):
        return self.get_queryset().two_lessons_remaining()

    def paid(self):
        return self.get_queryset().paid()

    def unpaid(self):
        return self.get_queryset().unpaid()

    def get_all(self):
        return self.get_queryset().all()


class PupilSubjectMatch(models.Model):
    class Meta:
        app_label = 'matchmaker'
        managed = False
        db_table = 'pupil_pupil_subject'

    id = models.IntegerField(primary_key=True)
    pupil = models.ForeignKey(Pupil)
    availabletutorsubject = models.ForeignKey(AvailableTutorSubject)

    def __unicode__(self):
        return '%s (%s)' % (self.pupil, self.availabletutorsubject)


class PupilProxy(Pupil):
    objects = PupilManager()

    class Meta:
        app_label = 'matchmaker'
        proxy = True
        verbose_name = 'pupil'
        verbose_name_plural = 'pupils'
        ordering = ('-created_at', 'surname', 'name')

    def __unicode__(self):
        return '%s: %s, %s for %s (%s)' % (
            self.created_at.strftime('%d-%m-%Y %H:%M'),
            self.surname,
            self.name,
            ', '.join(s.name for s in self.subject.all()),
            self.level_of_study
        )

    def get_number_of_tutors(self):
        return self.objects.all().__sizeof__();

    @property
    def needs_tutor(self):
        return self.unmatched_subjects.exists()

    @property
    def unmatched_subjects(self):
        # get subjects actively being tutored
        return self.subject.exclude(id__in=PupilTutorMatch.objects.filter(pupil=self).values_list('subject_id',
                                                                                                  flat=True))


class TutorProxy(Tutor):
    class Meta:
        app_label = 'matchmaker'
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

    class Meta:
        app_label = 'matchmaker'

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
        app_label = 'matchmaker'
        verbose_name = 'Request SMS'
        verbose_name_plural = "Request SMSes"

    requests = models.ManyToManyField(RequestForTutor)
    tutor = models.ForeignKey(TutorProxy)
    response_text = models.CharField(max_length=256, null=True, blank=True)
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
    sms_objects = RequestSMS.objects.filter(
        pk__in=[i.pk for i in kwargs['instance']]
    )
    if len(sms_objects) == 0:
        pass
    elif len(sms_objects) == 1:
        sms_obj = sms_objects[0]
        sms_obj.response_text = kwargs['text']
        sms_obj.response_timestamp = kwargs['timestamp']
        sms_obj.save()
    else:
        # match by code in response
        codes = [c[0].strip() for c in
                 re.findall(r'(\w{6,12}($|\s+))',
                            kwargs['text'],
                            re.DOTALL)]

        if sms_objects.filter(requests__code__in=codes).exists():
            sms_objects = sms_objects.filter(requests__code__in=codes)
        else:
            sms_objects = sms_objects.filter(response_text__isnull=True)
        sms_objects.update(response_text=kwargs['text'],
                           response_timestamp=kwargs['timestamp'])
