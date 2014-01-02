from django.conf.urls import *
from common import views

urlpatterns = patterns('',
                       url(r'^$', views.HomeView.as_view() ,name='home'),
                       )
