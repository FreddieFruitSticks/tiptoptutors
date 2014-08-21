import mimetypes

from django.db import models


class Document(models.Model):
    name = models.CharField(max_length=128,
                            null=True, blank=True,
                            editable=False)
    mime_type = models.CharField(max_length=128,
                                 null=True, blank=True,
                                 editable=False)
    data = models.BinaryField()
    created = models.DateTimeField(auto_now_add=True,
                                   editable=False)
    modified = models.DateTimeField(auto_now=True,
                                    editable=False)

    def save(self, *args, **kwargs):
        if self.name is not None:
            self.mime_type = mimetypes.guess_type(self.name)[0]
        super(Document, self).save(*args, **kwargs)
