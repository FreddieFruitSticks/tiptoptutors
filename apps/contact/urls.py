from django.conf.urls import *
from contact.views import ContactView, ContactSuccessView

urlpatterns = patterns('',
                       url(r'^contact/$', ContactView.as_view(), {}, name="contact"),
                       url(r'^contact/success/$', ContactSuccessView.as_view(), {},  name='contact-complete'),
                       )
