from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.views.generic import CreateView

from forms import ProgressReportForm
from tutor.models import Tutor


class ProgressReportView(CreateView):
    form_class = ProgressReportForm
    template_name = 'progress_reports/progress_report.html'

    def post(self, request, *args, **kwargs):
        print ('in post in view')
        if request.user is None:
            return render_to_response('progress_reports/user_does_not_exist.html')
        print(request.user)
        user = User.objects.get(username=request.user)
        tutor = Tutor.objects.get(user__id=user.id)
                


    def get_success_url(self):
        return reverse('registerlessonsuccess')


def prog_report_success(request):
    return render_to_response('progress_reports/registered_lesson_success.html')
