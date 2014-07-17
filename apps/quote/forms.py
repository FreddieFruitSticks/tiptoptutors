import os

from django.conf import settings
from django import forms
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from quote.models import Quote


class QuoteForm(forms.ModelForm):

    class Meta:
        model = Quote

    def save(self):
        html_content = render_to_string('quote/quote-email.html')
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject='Tip Top Tutors: Quote',
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[self.instance.email],
        )
        email.attach_alternative(html_content, 'text/html')
        doc_dir = os.path.join(os.path.dirname(__file__), 'data')
        email.attach_file(os.path.join(doc_dir, 'High school rates.pdf'))
        email.attach_file(os.path.join(doc_dir, 'University rates.pdf'))
        email.send(fail_silently=not settings.DEBUG)
        return super(QuoteForm, self).save()
