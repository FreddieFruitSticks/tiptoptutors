import random

from django.db import models

from pupil.models import Pupil
from tutor.models import Tutor
from option.models import AvailableTutorSubject


# numbers + lowercase + uppercase
REQUEST_CODE_CHARSET = [chr(i) for i in range(ord('0'), ord('9') + 1)] + \
                       [chr(i) for i in range(ord('a'), ord('z') + 1)] + \
                       [chr(i) for i in range(ord('A'), ord('Z') + 1)]


class SubjectManager(models.Manager):

    def get_queryset(self):
        qs = super(SubjectManager, self).get_queryset()
        return qs.select_related('subject')


class SubjectMixin(object):

    @property
    def subject_str(self):
        return ', '.join(self.subject.values_list('name', flat=True))

    def matching_subjects(self, subject_ids):
        return self.subject.filter(id__in=subject_ids)


class PupilProxy(Pupil, SubjectMixin):
    default_manager = SubjectManager()

    class Meta:
        proxy = True
        verbose_name = 'pupil'
        verbose_name_plural = 'pupils'
        ordering = ('-created_at', 'surname', 'name')

    def __unicode__(self):
        return '%s: %s for %s (%s)' % (self.created_at.strftime('%d-%m-%Y %H:%M'),
                                       self.name, self.subject_str,
                                       self.level_of_study)

    @property
    def has_tutor(self):
        return (self.tutor_id is not None)


class TutorProxy(Tutor, SubjectMixin):
    default_manager = SubjectManager()

    class Meta:
        proxy = True
        verbose_name = 'available tutor'
        verbose_name_plural = 'available tutors'

    def __unicode__(self):
        return '%s %s' % (self.name, self.surname)


class RequestForTutor(models.Model):
    '''
    This is the base class for tutor requests. In future, multiple
    communication media might be used to reach out to tutors. Only
    generic functionality should go here.
    '''
    pupil = models.ForeignKey(PupilProxy)
    subjects = models.ManyToManyField(AvailableTutorSubject)
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
    def generate_unique_code(length=12, charset=REQUEST_CODE_CHARSET):
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


class RequestSMS(models.Model):
    request = models.ForeignKey(RequestForTutor)
    tutor = models.ForeignKey(TutorProxy)
    delivery_status = models.CharField(max_length=16, default='unknown')
    response_text = models.CharField(max_length=32, null=True, blank=True)
    response_timestamp = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)

    @property
    def code(self):
        return request.code
