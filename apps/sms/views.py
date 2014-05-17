from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from .api import process_status_report, ClickatellException


class StatusCallbackView(View):
    http_method_names = ["post"]

    def post(self, request, *args, **kwargs):
        # return 400 with error message in response if DEBUG = True
        # otherwise always return 200 response
        try:
            process_status_report('Clickatell', request)
        except ClickatellException as e:
            if settings.DEBUG:
                return HttpResponseBadRequest(str(e))
        return HttpResponse()
