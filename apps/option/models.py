from django.db import models

class City(models.Model):
    name               = models.CharField(max_length=255, blank=False, null=False)

    def __unicode__(self):
        return self.name

class LevelOfStudy(models.Model):
    name               = models.CharField(max_length=255, blank=False, null=False)

    def __unicode__(self):
        return self.name
#
class AvailableTutorSubject(models.Model):
    name               = models.CharField(max_length=255, blank=False, null=False)

    class Meta:
        ordering = ('name', )

    def __unicode__(self):
        return self.name

