from django.views.generic.edit import FormView
from contact.forms import ContactForm


class Contactview(FormView):

    form_class = ContactForm
    success_url = ('success')
    template_name = "contact/contact.html"

    def form_valid(self, form):
        form.save(commit=True)
        return super(Contactview, self).form_valid(form)