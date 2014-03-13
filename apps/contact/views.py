from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from contact.forms import ContactForm
from django.http import HttpResponseRedirect
from contact.models import Contact


class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contact/contact.html"
    success_url = "/contact/success/"

    def form_valid(self, form):
        super(ContactView,self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class ContactSuccessView(TemplateView):
    template_name = "contact/contact-complete.html"