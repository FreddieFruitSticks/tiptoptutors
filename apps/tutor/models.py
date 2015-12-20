from django import forms
from django.db import models
from common.models import Document
from option.models import AvailableTutorSubject


class Tutor(models.Model):
    TUTOR_STATUS = (
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Pending', 'Pending'),
    )
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    # admin tools
    comment = models.TextField(null=True, blank=True)
    # front end display
    # TODO - make next 6 fields required (show * in form)
    name = models.CharField(max_length=20, verbose_name="name")
    surname = models.CharField(max_length=20, verbose_name="surname")
    gender = models.CharField(max_length=6, verbose_name="gender",
                              choices=GENDER_CHOICES)
    email = models.EmailField(verbose_name="email")
    mobile = models.CharField(max_length=10, verbose_name="mobile number")
    subject = models.ManyToManyField(AvailableTutorSubject, verbose_name="subject")
    transport = models.BooleanField(verbose_name="Transport",
                                    default=False,
                                    help_text="Do you have your own transport?")
    id_passport = models.CharField(max_length=20, verbose_name="ID/passport number")
    id_doc = models.ForeignKey('common.Document',
                               verbose_name="ID",
                               help_text="Identification document with a photo is required.",
                               related_name="id_tutors",
                               null=True)  # not blank=True on purpose
    cv = models.ForeignKey('common.Document',
                           verbose_name="CV",
                           blank=True, null=True,
                           related_name="cv_tutors")
    academic = models.ForeignKey('common.Document',
                                 verbose_name="Academic transcript",
                                 blank=True, null=True,
                                 related_name="academic_tutors",
                                 help_text="If you don't have a university-level "
                                           "transcript for the subjects you want to tutor, "
                                           "attach your matric results instead.")
    status = models.CharField(max_length=10, choices=TUTOR_STATUS, default='2')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.name + " " + self.surname
