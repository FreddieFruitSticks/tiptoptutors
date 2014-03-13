from django.db import models

from pupil.models import Pupil
from tutor.models import Tutor


class PupilProxy(Pupil):

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
    def subject_str(self):
        return ', '.join(self.subject.values_list('name', flat=True))

    @property
    def has_tutor(self):
        return (self.tutor_id is not None)


class TutorProxy(Tutor):
    
    class Meta:
        proxy = True
        verbose_name = 'available tutor'
        verbose_name_plural = 'available tutors'
