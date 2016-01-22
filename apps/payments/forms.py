from django import forms

from models import ProgressReport


class ProgressReportForm(forms.ModelForm):
    pupil_pin = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = ProgressReport
        exclude = ('lesson',)

    def is_valid(self):
        print('in form_valid in form')
        valid = super(ProgressReportForm, self).is_valid()
        if not valid:
            return valid
        return valid

