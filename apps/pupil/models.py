from django.db import models

from option.models import City, LevelOfStudy, AvailableTutorSubject
from tutor.models import Tutor


class PupilTutorMatch(models.Model):
    '''
    Stores information regarding a particular pupil-tutor matchup,
    including the start and end dates of the tutoring period.
    '''
    pupil = models.ForeignKey('Pupil', null=True)
    tutor = models.ForeignKey(Tutor, null=True)
    # a matchup must be create per subject
    subject = models.ForeignKey(AvailableTutorSubject)

    price = models.CharField(max_length=20, null=True, blank=True)
    lesson = models.CharField(max_length=20, verbose_name="number of lessons", null=True, blank=True)
    lessons_bought = models.IntegerField(blank=True, null=True, default=0)
    last_bought_updated = models.DateField(verbose_name="bought updated", null=True, blank=True, db_index=True)
    lessons_taught = models.IntegerField(blank=True, null=True, default=0)
    last_taught_updated = models.DateField(verbose_name="taught updated", null=True, blank=True, db_index=True)

    lessons_remaining = models.IntegerField(verbose_name="lessons remaining", null=True, blank=True)
    readonly_fields = (lessons_remaining,)

    @property
    def is_active(self):
        return (self.lessons_bought > 0) \
               and (self.lessons_bought - self.lessons_taught > 0)

    @property
    def get_prog_report_unicode(self):
        return '%s %s (%s)' % (self.pupil.name, self.pupil.surname, self.subject.name)

    def __unicode__(self):
        return '%s - %s (%s)' % (self.pupil, self.tutor, self.subject)

    def save(self, **kwargs):
        self.lessons_remaining = self.lessons_bought - self.lessons_taught
        super(PupilTutorMatch, self).save()


class Pupil(models.Model):
    tutor = models.ManyToManyField(Tutor, null=True, blank=True,
                                   through=PupilTutorMatch)
    name = models.CharField(max_length=20, verbose_name="Pupil name")
    surname = models.CharField(max_length=20)
    email = models.EmailField()
    contact_number = models.CharField(max_length=15)
    subject = models.ManyToManyField(AvailableTutorSubject)
    level_of_study = models.ForeignKey(LevelOfStudy)
    street = models.CharField(max_length=20)
    suburb = models.CharField(max_length=20)
    city = models.ForeignKey(City)
    # TODO - sort out commented out fields
    # available_times = models.TextField(blank=True, null=True)
    requirement = models.TextField(verbose_name="personal requirements", blank=True, null=True)
    # time_and_day    = models.TextField(verbose_name="times and days", blank=True, null=True)

    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return '%s %s' % (self.name, self.surname)

    @property
    def full_name(self):
        return '%s %s' % (self.name, self.surname)


class PupilPin(models.Model):
    pin = models.CharField(max_length=4)
    pupil = models.ForeignKey(Pupil)
    readonly_fields = (pin, pupil,)

    def __unicode__(self):
        return '%s %s: %s' % (self.pupil.name, self.pupil.surname, self.pin)
