from django.contrib.auth.models import User
from django.db import models

from option.models import AvailableTutorSubject


class TutorQuerySet(models.query.QuerySet):
    def active_tutor(self):
        return self.filter(pupiltutormatch__isnull=False).distinct()

    def inactive_tutor(self):
        return self.filter(pupiltutormatch__isnull=True).distinct()


class TutorManager(models.Manager):
    def get_queryset(self):
        return TutorQuerySet(self.model, using=self._db)

    def active_tutor(self):
        return self.get_queryset().active_tutor()

    def inactive_tutor(self):
        return self.get_queryset().inactive_tutor()


class Tutor(models.Model):
    objects = TutorManager()

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
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, default=None)
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
    status = models.CharField(max_length=10, choices=TUTOR_STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __unicode__(self):
        return self.name + " " + self.surname
