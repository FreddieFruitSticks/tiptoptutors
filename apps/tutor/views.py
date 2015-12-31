# from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from tutor.forms import TutorForm


class TutorView(CreateView):
    form_class = TutorForm
    template_name = "tutor/tutor.html"

    def get_success_url(self):
        from django.core.urlresolvers import reverse
        return reverse('tutor-success')


class TutorSuccessView(TemplateView):
    template_name = "tutor/tutor-success.html"


def tutor_login_frontpage(request):
    form_class = TutorForm
    template_name = "tutor/tutor.html"

    return render_to_response(template_name, {'form': form_class})