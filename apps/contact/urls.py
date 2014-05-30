from django.conf.urls import *
from contact.views import ContactMeView, ContactSuccessView

urlpatterns = patterns('',
                       url(r'^contact/$', ContactMeView.as_view(), {}, name="contact"),
                       url(r'^contact/success/$', ContactSuccessView.as_view(), {},  name='contact-complete'),
                       )
