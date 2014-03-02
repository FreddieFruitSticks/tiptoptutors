from django.db import models
from option.models import AvailableTutorSubject
from student.models import Student


class Tutor(models.Model):

    #admin tools
    student     = models.ManyToManyField(Student)
    lesson      = models.CharField(verbose_name='lessons remaining', max_length=20)
    comment     = models.TextField()
    #front end display
    name        = models.CharField(max_length=20, verbose_name="first name")
    surname     = models.CharField(max_length=20)
    email       = models.EmailField(max_length=25)
    mobile      = models.CharField(max_length=10)
    id_passport = models.CharField(max_length=20, verbose_name="id/passport number")
    subject     = models.ManyToManyField(AvailableTutorSubject)
    transport   = models.BooleanField(verbose_name="own transport?")
    id_doc      = models.FileField(verbose_name="id", upload_to="media/cv")
    cv          = models.FileField(blank=True, null=True, upload_to="media/cv")
    academic    = models.FileField(verbose_name="academic transcript",blank=True, null=True, upload_to="media/academic/")

    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
