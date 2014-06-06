from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View

from .api import process_status_report, process_reply, SMSApiException


DEFAULT_SMS_API = 'BulkSMS'


class StatusCallbackView(View):
    http_method_names = ["post", "get"]

    def post(self, request, *args, **kwargs):
        # return 400 with error message in response if DEBUG = True
        # otherwise always return 200 response
        try:
            process_status_report('Clickatell', request)
        except SMSApiException as e:
            if settings.DEBUG:
                return HttpResponseBadRequest(str(e))
        return HttpResponse()

    def get(self, request, *args, **kwargs):
        try:
            process_status_report('BulkSMS', request)
        except SMSApiException as e:
            if settings.DEBUG:
                return HttpResponseBadRequest(str(e))
        return HttpResponse('OK')


class ReplyCallbackView(View):
    http_method_names = ["post", "get"]

    def post(self, request, *args, **kwargs):
        try:
            process_reply('Clickatell', request)
        except SMSApiException as e:
            if settings.DEBUG:
                return HttpResponseBadRequest(str(e))
        return HttpResponse()

    def get(self, request, *args, **kwargs):
        try:
            process_reply('BulkSMS', request)
        except SMSApiException as e:
            if settings.DEBUG:
                return HttpResponseBadRequest(str(e))
        return HttpResponse('OK')
