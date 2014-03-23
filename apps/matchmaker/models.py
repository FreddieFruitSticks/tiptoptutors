from django.db import models

from pupil.models import Pupil
from tutor.models import Tutor


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
