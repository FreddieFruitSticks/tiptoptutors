from django.conf.urls import *

from .views import StatusCallbackView


urlpatterns = patterns('',
    url(
        r'^status-callback/$',
        StatusCallbackView.as_view(),
        name="sms-status-callback"
    ),
)
