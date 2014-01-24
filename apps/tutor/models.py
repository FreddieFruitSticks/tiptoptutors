from django.db import models

class Tutor(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    email = models.EmailField(max_length=255, blank=False, null=False)

    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
