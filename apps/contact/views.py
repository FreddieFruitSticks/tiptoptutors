from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from contact.forms import ContactForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from contact.models import Contact

class ContactView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = "contact/contact.html"

    def form_valid(self, form):
        super(ContactView,self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse("success")

class SuccessView(TemplateView):
    template_name = "contact/success.html"