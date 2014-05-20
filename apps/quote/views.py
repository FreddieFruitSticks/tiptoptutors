from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from quote.forms import QuoteForm
from django.http import HttpResponseRedirect
from quote.models import Quote


class QuoteView(CreateView):
    model = Quote
    form_class = QuoteForm
    template_name = "quote/quote.html"
    success_url = "/quote/success/"

    def form_valid(self, form):
        super(QuoteView,self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())




class QuoteSuccessView(TemplateView):
    template_name = "quote/quote-complete.html"