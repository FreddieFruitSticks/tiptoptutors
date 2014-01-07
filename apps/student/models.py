from django.db import models
from option.models import City, LevelOfStudy


class Student(models.Model):
    name            = models.CharField(max_length=20)
    surname         = models.CharField(max_length=20)
    email           = models.EmailField()
    contact_number  = models.CharField(max_length=15)
    subject         = models.CharField(max_length=50)
    level_of_study  = models.ForeignKey(LevelOfStudy)
    street          = models.CharField(max_length=20)
    suburb          = models.CharField(max_length=20)
    city            = models.ForeignKey(City)
    requirement     = models.TextField(verbose_name="personal requirements", blank=True, null=True)

    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
