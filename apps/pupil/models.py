from datetime import datetime

from django.db import models

from option.models import City, LevelOfStudy, AvailableTutorSubject
from tutor.models import Tutor


class PupilTutorMatch(models.Model):
    '''
    Stores information regarding a particular pupil-tutor matchup,
    including the start and end dates of the tutoring period.
    '''
    pupil = models.ForeignKey('Pupil')
    tutor = models.ForeignKey(Tutor)
    subject = models.ManyToManyField(AvailableTutorSubject)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    @property
    def is_active(self):
        return (self.start_date <= datetime.utcnow().date() <= self.end_date)

    def end_now(self):
        self.end_date = datetime.utcnow().date()
        self.save()

    def start_now(self):
        self.start_date = datetime.utcnow().date()
        self.save()


class Pupil(models.Model):
    tutor           = models.ManyToManyField(Tutor, null=True, blank=True,
                                             through=PupilTutorMatch)
    name            = models.CharField(max_length=20)
    surname         = models.CharField(max_length=20)
    email           = models.EmailField()
    contact_number  = models.CharField(max_length=15)
    subject         = models.ManyToManyField(AvailableTutorSubject)
    level_of_study  = models.ForeignKey(LevelOfStudy)
    street          = models.CharField(max_length=20)
    suburb          = models.CharField(max_length=20)
    city            = models.ForeignKey(City)
    # available_times = models.TextField(blank=True, null=True)
    requirement     = models.TextField(verbose_name="personal requirements", blank=True, null=True)

    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.surname)
