from django import forms
from django.contrib import admin

import models


class DocumentForm(forms.ModelForm):
    file = forms.FileField()

    class Meta:
        model = models.Document
        fields = ['is_public']

    def save(self, commit=True):
        self.instance.set_file(self.cleaned_data['file'])
        return super(DocumentForm, self).save(commit)


class DocumentAdmin(admin.ModelAdmin):
    list_display = ['name', 'mime_type', 'is_public', 'created', 'modified', 'url']
    list_editable = ['is_public']
    form = DocumentForm

    def url(self, obj):
        return '<a href="%s">Download</a>' % obj.get_absolute_url()
    url.allow_tags = True
    url.short_description = 'URL'

admin.site.register(models.Document, DocumentAdmin)
