from django import forms
from django.contrib import admin

import models


class DocumentForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = models.Document

    def save(self, commit=True):
        self.instance.set_file(self.cleaned_data['file'])
        return super(DocumentForm, self).save(commit)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'mime_type', 'created', 'modified']
    form = DocumentForm


admin.site.register(models.Document, DocumentAdmin)
