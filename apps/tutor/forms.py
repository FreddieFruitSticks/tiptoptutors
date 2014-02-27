from django import forms
from tutor.models import Tutor


class TutorForm(forms.ModelForm):

    class Meta:
        model = Tutor
        exclude = ('student', 'lesson', 'comment')
