from django import forms

from pupil.models import Pupil


class PupilForm(forms.ModelForm):
    class Meta:
        model = Pupil
        exclude = ('tutor',)
