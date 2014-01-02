from django.conf.urls import *
from common import views

urlpatterns = patterns('',
                       url(r'^$', views.HomeView.as_view() ,name='home'),
                       url(r'^about/$', views.AboutView.as_view() ,name='about'),
                       url(r'^how-this-works/$', views.HowThisWorksView.as_view() ,name='how-this-works'),
                       url(r'^subjects/$', views.SubjectsView.as_view() ,name='subjects'),
                       )
