from django.conf.urls import *

from .views import StatusCallbackView, ReplyCallbackView


urlpatterns = patterns('',
    url(
        r'^status-callback/$',
        StatusCallbackView.as_view(),
        name="sms-status-callback"
    ),
    url(
        r'^reply-callback/$',
        ReplyCallbackView.as_view(),
        name="sms-reply-callback"
    )
)
