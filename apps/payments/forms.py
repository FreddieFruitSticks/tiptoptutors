from django import forms

from models import ProgressReport


class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
        fields = ['homework_status', 'homework_summary', 'student_summary']
        # exclude = ('lesson',)
        # widgets = {
        #     'homework_summary': Textarea(attrs={'placeholder': 'name'}),
        # }

    def __init__(self, *args, **kwargs):
        pupils = kwargs.pop('student')
        super(ProgressReportForm, self).__init__(*args, **kwargs)

        self.fields['pupil'] = forms.ChoiceField(choices=pupils, initial=None)
        self.fields['pupil_pin'] = forms.CharField(widget=forms.PasswordInput)

        # def is_valid(self):
        #     valid = super(ProgressReportForm, self).is_valid()
        #     if not valid:
        #         return valid
        #     return valid
