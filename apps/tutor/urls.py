from django.conf.urls import *
from tutor.views import TutorView, TutorSuccessView, tutor_login_frontpage

urlpatterns = patterns('',
                       url(r'^tutor/$', tutor_login_frontpage, name="tutor"),
                       url(r'^tutor-success/$', TutorSuccessView.as_view(),  name='tutor-success'),
                       )
