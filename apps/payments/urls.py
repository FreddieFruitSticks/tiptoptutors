from django.conf.urls import url, patterns
from views import ProgressReportView
from payments import views

urlpatterns = patterns('',
                       url(r'^progressreport/', ProgressReportView.as_view(), name='registerlesson'),
                       url(r'^progressreportsuccess/', views.prog_report_success, name='registerlessonsuccess')

                       )
