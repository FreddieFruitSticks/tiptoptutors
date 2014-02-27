from django.db import models
from option.models import AvailableTutorSubject
from student.models import Student


class Tutor(models.Model):

    #admin tools
    student     = models.ManyToManyField(Student)
    lesson      = models.CharField(verbose_name='lessons remaining', max_length=20)
    comment     = models.TextField()
    #front end display
    name        = models.CharField(max_length=20)
    surname     = models.CharField(max_length=20)
    mobile      = models.CharField(max_length=10)
    email       = models.EmailField(max_length=25)
    subject     = models.ManyToManyField(AvailableTutorSubject)
    cv          = models.FileField(blank=True, null=True, upload_to="media/cv")
    academic    = models.FileField(blank=True, null=True, upload_to="media/academic/")

    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
