from django import forms

from models import ProgressReport


class ProgressReportForm(forms.ModelForm):
    class Meta:
        model = ProgressReport
