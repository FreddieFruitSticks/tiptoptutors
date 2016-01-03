from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from tutor.forms import TutorDetailsForm


class TutorView(CreateView):
    form_class = TutorDetailsForm
    template_name = "tutor/tutor.html"

    def form_valid(self, form):
        tutor = form.save(commit=False)
        tutor.user = User.objects.get(username=self.request.user)
        tutor.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        from django.core.urlresolvers import reverse
        return reverse('tutor-success')


class TutorSuccessView(TemplateView):
    template_name = "tutor/tutor-success.html"


class TutorInvalid(TemplateView):
    template_name = 'tutor/tutor-invalid.html'

