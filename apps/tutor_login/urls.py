from django.conf.urls import patterns, url
from tutor_login import views

urlpatterns = patterns('',
                       url(r'^login/$', views.register_user, name='login'),
                       url(r'^auth/$', views.auth_view, name='auth'),
                       url(r'^loggedin/$', views.loggedin, name='loggedin'),
                       url(r'^logout/$', views.logout, name='logout')
                       )
