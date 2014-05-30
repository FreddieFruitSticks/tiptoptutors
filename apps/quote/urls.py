from django.conf.urls import *
from quote.views import QuoteView, QuoteSuccessView

urlpatterns = patterns('',
                       url(r'^quote/$', QuoteView.as_view(), {}, name="quote"),
                       url(r'^quote/success/$', QuoteSuccessView.as_view(), {},  name='quote-complete'),
                       )

