from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from contact.views import ContactView
from pupil.forms import PupilForm
from django.http import HttpResponseRedirect
from pupil.models import Pupil


class PupilView(CreateView):
    model = Pupil
    form_class = PupilForm
    template_name = "pupil/pupil.html"
    success_url = "/pupil/success/"

    def form_valid(self, form):
        super(PupilView,self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class PupilSuccessView(TemplateView):
    template_name = "pupil/pupil-complete.html"