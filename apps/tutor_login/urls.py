from django.conf.urls import patterns, url
from tutor_login import views

urlpatterns = patterns('',
                       url(r'^login/$', views.register_user, name='login'),
                       url(r'^auth/$', views.auth_view, name='auth'),
                       url(r'^loggedin/$', views.loggedin, name='loggedin'),
                       url(r'^logout/$', views.logout, name='logout'),
                       url(r'^pupilsummary/', views.tutor_pupil_summary, name="tutorsummary"),
                       url(r'^invalidlogin/', views.invalid_login, name="invalidlogin"),

                       url(r'^tutorfaq/', views.tutor_faq, name="tutorfaq"),
                       url(r'^registerlesson/', views.register_lesson, name="registerlesson"),
                       url(r'^pupilscredits/', views.pupil_credits, name="pupilscredits"),
                       url(r'^lessonhistory/', views.lesson_history, name="lessonhistory")
                       )
