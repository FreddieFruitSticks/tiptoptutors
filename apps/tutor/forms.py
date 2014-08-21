from django import forms
from tutor.models import Tutor


class TutorForm(forms.ModelForm):

    class Meta:
        model = Tutor
        exclude = ('lesson', 'comment', 'status')
        widgets = {
            'id_doc': forms.FileInput,
            'cv': forms.FileInput,
            'academic': forms.FileInput,
        }
