from django.db import models


# from payments.models import TutorFee


class City(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    def __unicode__(self):
        return self.name


class LevelOfStudy(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)
    rate_category = models.ForeignKey('payments.TutorFee', null=True, blank=True)

    def __unicode__(self):
        return '%s' % self.name


#
class AvailableTutorSubject(models.Model):
    name = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        ordering = ('name',)

    def __unicode__(self):
        return self.name
