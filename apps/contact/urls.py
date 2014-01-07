from django.conf.urls import *
from contact.views import ContactView, SuccessView

urlpatterns = patterns('',
                       url(r'^contact/$', ContactView.as_view(), {}, name="contact"),
                       url(r'^success/$', SuccessView.as_view(), {},  name='success'),
                       )
