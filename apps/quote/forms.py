import os

from django.conf import settings
from django import forms
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from common.models import Document
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
        self.attach_file_from_documents(email, 'High school rates.pdf')
        self.attach_file_from_documents(email, 'University rates.pdf')
        email.send(fail_silently=not settings.DEBUG)
        return super(QuoteForm, self).save()

    def attach_file_from_documents(self, email, name):
        doc = Document.objects.filter(name__iexact=name) \
                              .order_by('-modified')[:1][0]
        path = '/tmp/%s' % name
        with open(path, 'wb') as f:
            f.write(doc.data)
        email.attach_file(path)
