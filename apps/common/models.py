import os
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

    def set_file(self, file_obj):
        self.name = os.path.basename(file_obj.name)
        self.data = file_obj.read()
        self.mime_type = mimetypes.guess_type(self.name)[0]

    @classmethod
    def create_from_file(cls, file_obj):
        doc = cls()
        doc.set_file(file_obj)
        doc.save()
        return doc

    def __unicode__(self):
        return self.name
