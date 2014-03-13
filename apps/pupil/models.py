from django.db import models
from option.models import City, LevelOfStudy, AvailableTutorSubject
from tutor.models import Tutor


class Pupil(models.Model):
    tutor           = models.ForeignKey(Tutor, null=True, blank=True)
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
