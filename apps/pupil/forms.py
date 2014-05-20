from django import forms
from django.http import HttpResponseRedirect
from pupil.models import Pupil


class PupilForm(forms.ModelForm):


    class Meta:
        model = Pupil
        exclude = ('tutor',)

