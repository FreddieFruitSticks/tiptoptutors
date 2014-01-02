from django.conf.urls import *
from tutor.views import TutorView, TutorSuccessView


urlpatterns = patterns('',
                       url(r'^tutor/$', TutorView.as_view(), name="tutor"),
                       url(r'^tutor-success/$', TutorSuccessView.as_view(),  name='tutor-success'),
                       )
