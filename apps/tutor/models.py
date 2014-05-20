from django.db import models
from option.models import AvailableTutorSubject

class Tutor(models.Model):
    TUTOR_STATUS = (
    ('Accepted', 'Accepted'),
    ('Declined', 'Declined'),
    ('Pending', 'Pending'),
    )
    #admin tools
    comment     = models.TextField(null=True, blank=True)
    #front end display
    name        = models.CharField(max_length=20, verbose_name="name *")
    surname     = models.CharField(max_length=20, verbose_name="surname *")
    email       = models.EmailField(max_length=25, verbose_name="email *")
    mobile      = models.CharField(max_length=10, verbose_name="mobile *")
    id_passport = models.CharField(max_length=20, verbose_name="id/passport number")
    subject     = models.ManyToManyField(AvailableTutorSubject, verbose_name="subject *")
    transport   = models.BooleanField(verbose_name="own transport?", default=False)
    id_doc      = models.FileField(verbose_name="id *", upload_to="media/cv")
    cv          = models.FileField(blank=True, null=True, upload_to="media/cv")
    academic    = models.FileField(verbose_name="academic* transcript ", blank=True, null=True, upload_to="media/academic/")
    status = models.CharField(max_length=10, choices=TUTOR_STATUS, default='2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name
