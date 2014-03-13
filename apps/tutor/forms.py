from django import forms
from tutor.models import Tutor


class TutorForm(forms.ModelForm):

    RADIO_CHOICES = (
        ('male', "male"),
        ('female', "female: "),
    )

    gender = forms.ChoiceField(widget=forms.RadioSelect(),choices=RADIO_CHOICES)

    class Meta:
        model = Tutor
        exclude = ('lesson', 'comment', 'status')
