from django.conf.urls import *
from student.views import StudentView, StudentSuccessView

urlpatterns = patterns('',
                       url(r'^student/$', StudentView.as_view(), {}, name="student"),
                       url(r'^student-success/$', StudentSuccessView.as_view(), {},  name='student-success'),
                       )

