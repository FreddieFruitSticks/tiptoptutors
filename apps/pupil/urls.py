from django.conf.urls import *
from pupil.views import PupilView, PupilSuccessView

urlpatterns = patterns('',
                       url(r'^pupil/$', PupilView.as_view(), {}, name="pupil"),
                       url(r'^pupil/success/$', PupilSuccessView.as_view(), {}, name='pupil-complete'),
                       )
