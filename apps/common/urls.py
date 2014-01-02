from django.conf.urls import *
from common import views

urlpatterns = patterns('',
                       url(r'^$', views.HomeView.as_view() ,name='home'),
                       url(r'^about/$', views.AboutView.as_view() ,name='about'),
                       )
