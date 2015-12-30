from django.conf.urls import *
from tutor.views import TutorView, TutorSuccessView, tutor_view_form

urlpatterns = patterns('',
                       url(r'^tutor/$', tutor_view_form, name="tutor"),
                       url(r'^tutor-success/$', TutorSuccessView.as_view(),  name='tutor-success'),
                       )
