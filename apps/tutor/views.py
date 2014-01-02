from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.http import HttpResponseRedirect
from tutor.forms import TutorForm


class TutorView(FormView):

    form_class = TutorForm
    template_name = "tutor/tutor.html"
    success_url = ('/tutor-success')

    def form_valid(self, form):
        super(TutorView,self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class TutorSuccessView(TemplateView):
    template_name = "tutor/tutor-success.html"
