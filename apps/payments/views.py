from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import CreateView

from forms import ProgressReportForm


class ProgressReportView(CreateView):
    form_class = ProgressReportForm
    template_name = 'progress_reports/progress_report.html'

    def get_success_url(self):
        return reverse('registerlessonsuccess')


def prog_report_success(request):
    return render('register_lesson_success.html')
