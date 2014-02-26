from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False, verbose_name="your name")
    email = models.EmailField(max_length=255, blank=False, null=False)
    message = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name

