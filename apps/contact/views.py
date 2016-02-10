from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from contact.forms import ContactForm
from django.http import HttpResponseRedirect
from contact.models import Contact


# class ContactMeView(CreateView):
#     model = Contact
#     form_class = ContactForm
#     template_name = "contact/contact.html"
#     success_url = "/contact/success/"
#
#     def get_subject(self, form):
#         return "Contact from MySite"
#
#     def get_from_email(self, form):
#         return "MySite <no-reply@example.com>"
#
#     def get_headers(self, form):
#         return {'Reply-To': u"{0}<{1}>".format(form.cleaned_data['name'], form.cleaned_data['email'])}
#
#     def form_valid(self, form):
#         super(ContactMeView, self).form_valid(form)
#         return HttpResponseRedirect(self.get_success_url())


class ContactSuccessView(TemplateView):
    template_name = "contact/contact-complete.html"


class ContactMeView(TemplateView):
    template_name = "contact/contact.html"
    success_url = "/contact/success/"
