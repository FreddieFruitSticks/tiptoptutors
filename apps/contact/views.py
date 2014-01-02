from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from contact.forms import ContactForm
from django.http import HttpResponseRedirect

class ContactView(FormView):

    form_class = ContactForm
    template_name = "contact/contact.html"
    success_url = ('/success')

    def form_valid(self, form):
        super(ContactView,self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class SuccessView(TemplateView):
    template_name = "contact/success.html"