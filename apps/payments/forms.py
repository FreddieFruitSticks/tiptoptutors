import random
from django import forms

from models import ProgressReport


class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        fields = ['homework_status', 'homework_summary', 'student_summary', 'duration']

    def __init__(self, *args, **kwargs):
        pupils = kwargs.pop('student')

        super(ProgressReportForm, self).__init__(*args, **kwargs)
        self.fields['pupil'] = forms.ChoiceField(choices=pupils)

        self.fields['pupil_pin'] = forms.CharField(widget=forms.PasswordInput, label='Pupil pin')


def get_random_number():
    pin = ''
    for i in range(0, 6):
        num = random.randint(0, 9)
        pin += str(num)

    return pin
