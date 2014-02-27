from django.db import models
from student.models import Student


class Tutor(models.Model):
    student = models.ManyToManyField(Student,blank=True, null=True, related_name="student")
    lessons_remaining = models.CharField(max_length=255,blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    # surname
    # mobile_number
    email = models.EmailField(max_length=255, blank=False, null=False)
    # tutoring_subjects
    tutoring_areas = models.CharField(max_length=200, blank=False, null=False)
    # cv = models.FileField(blank=True, null=True,upload_to="/media/cv")
    # academic_transcript = models.FileField(upload_to="/media/at")

    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
