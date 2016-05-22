import random
from django import forms

from models import ProgressReport


class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        fields = ['homework_status', 'homework_summary', 'student_summary']

    def __init__(self, *args, **kwargs):
        pupils = kwargs.pop('student')
        super(ProgressReportForm, self).__init__(*args, **kwargs)
        random_num = get_random_number()
        self.fields['pupil'] = forms.ChoiceField(choices=pupils, initial=None)
        # self.fields['pass'] = forms.CharField(widget=forms.PasswordInput, widget=forms.HiddenInput)
        # self.fields['pupil_pin'] = forms.CharField(widget=forms.PasswordInput, label='Pupil pin')
        # self.fields['pupil_pin'+random_num] = self.fields['pupil_pin']
        # del self.fields['pupil_pin']

        # self.fields['pupil_pin'].widget.attrs \
        #     .update({
        #     'autocomplete': 'off'
        # })


def get_random_number():
    pin = ''
    for i in range(0, 6):
        num = random.randint(0, 9)
        pin += str(num)

    return pin
