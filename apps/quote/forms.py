from django import forms
from quote.models import Quote


class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote

