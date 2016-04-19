from django.contrib.auth import get_user_model
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
        user = get_user_model().objects.get(username=self.request.user);
        tutor.user = user
        tutor.name = user.first_name
        tutor.surname = user.last_name
        tutor.email = user.email
        tutor.save()
        super(TutorView, self).form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        from django.core.urlresolvers import reverse
        return reverse('tutor-success')


class TutorSuccessView(TemplateView):
    template_name = "tutor/tutor-success.html"


class TutorInvalid(TemplateView):
    template_name = 'tutor/tutor-invalid.html'
