from django import forms
from django.db import models

from common.forms import RelatedDocumentsForm
from tutor.models import Tutor


class TutorDetailsForm(RelatedDocumentsForm):
    # def __init__(self, *args, **kwargs):
    #     self.request = kwargs.pop('request', None)
    #     print 'in tutor form: '
    #     # print self.request.POST.get('username', '')
    #     super(TutorDetailsForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Tutor
        exclude = ('lesson', 'comment', 'status', 'user')
        # widgets = {'user': forms.HiddenInput(), 'email': forms.HiddenInput()}
    #
    # def save(self, commit=True):
    #     tutor = super(TutorDetailsForm, self).save(commit=False)
    #     tutor.user = self.cleaned_data[self.request.user]
    #     # tutor.email = self.cleaned_data[self.request.POST.get('username', '')]
    #     if commit:
    #         tutor.save()
    #     return tutor
