import json
import re
import time
from datetime import datetime, timedelta

from django.conf import settings, ImproperlyConfigured
from django.dispatch import Signal
from django.utils import timezone

import pytz
import requests

from sms.models import SMS


sms_reply_received = Signal(providing_args=['instance', 'text', 'timestamp'])


class SMSApi(object):
    '''
    Base class for integrating with 3rd-party SMS service.
    '''

    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url

    def send(self, numbers, message):
        '''
        Returns [(apimsgid, address), ...] for each number provided.
        '''
        raise NotImplementedError

    def process_reply(self, request):
        '''
        Extracts and returns (message_id, address, text, datetime)
        from request.
        '''
        raise NotImplementedError

    def process_status_report(self, request):
        '''
        Extracts and returns (message_id, address, status)
        from request.
        '''
        raise NotImplementedError


class InvalidAPIError(ValueError):
    pass


class ClickatellException(Exception):
    pass


class Clickatell(SMSApi):

    SESSION_TIMEOUT = 10 * 60  # Clickatell docs say 15 minutes
    ERROR_REGEX = re.compile(r'ERR:\s*(?P<err_no>\d+),\s*(?P<err_description>.*)')
    SESSION_REGEX = re.compile(r'OK:\s*(?P<session_id>.*)')
    SEND_REGEX = re.compile(r'ID:\s*(?P<apimsgid>\w+)(\s*To:\s*(?P<address>[0-9+]+))?[\s\n\r]*')
    STATUSES = {
        '003': 'Delivered to gateway',
        '004': 'Received by recipient',
        '005': 'Error with message',
        '007': 'Error delivering message',
        '009': 'Routing error',
        '010': 'Message expired',
        '012': 'Out of credit',
    }

    def __init__(self, endpoint_url, api_id, username, password, sender_id=None):
        self.endpoint_url = endpoint_url
        self.api_id = api_id
        self.username = username
        self.password = password
        self.sender_id = sender_id
        self.session_id = None

    def __eq__(self, other):
        # for testing
        return self.api_id == other.api_id

    def __ne__(self, other):
        # for testing
        return self.api_id != other.api_id

    def _request(self, rel_path, params):
        if self.session_id is None or (self.last_session_activity - time.time()
                                       > Clickatell.SESSION_TIMEOUT):
            self.session_id = self._start_session()

        current_time = time.time()
        params = params.copy()
        params['session_id'] = self.session_id
        resp = requests.get('%s/%s' % (self.endpoint_url, rel_path),
                            params=params)
        self.last_session_activity = current_time

        self._check_error_and_raise(resp)

        return resp.text

    def _check_error_and_raise(self, response):
        if response.status_code != 200:
            raise ClickatellException("HTTP %s: %s" % (response.status_code,
                                                       response.text))
        match = Clickatell.ERROR_REGEX.match(response.text)
        if match:
            raise ClickatellException("Error %s: %s" % (match.group('err_no'),
                                                        match.group('err_description')))

    def _start_session(self):
        resp = requests.get('%s/auth' % self.endpoint_url,
                            params={'api_id': self.api_id,
                                    'user': self.username,
                                    'password': self.password})

        self._check_error_and_raise(resp)

        return Clickatell.SESSION_REGEX.match(resp.text).group('session_id')

    def send(self, numbers, message, enable_reply=False):
        '''
        Returns [(apimsgid, address), ...] for each number provided.
        Raises ClickatellException if a request fails.
        Note: Clickatell requires numbers in international format without
        the leading '+'.
        '''
        addresses = ','.join(numbers)
        params = {
            'to': addresses,
            'text': message,
            'callback': '7',  # return intermediate, final and error statuses,
        }
        if enable_reply:
            # make Clickatell route via a registered short code
            params['mo'] = '1'
            if self.sender_id is not None:
                # specify the particular short code (in case there is more than one)
                params['from'] = self.sender_id
        body = self._request('sendmsg', params)
        matches = Clickatell.SEND_REGEX.findall(body)
        if len(numbers) == 1:
            return [(g[0], numbers[0]) for g in matches]
        return [(g[0], g[2]) for g in matches]

    def process_status_report(self, request):
        '''
        Extracts and returns (message_id, address, status)
        from request.
        '''
        # We set up Clickatell to use HTTP POSTs
        if request.method != "POST":
            raise ClickatellException("Invalid request type")
        try:
            fields = json.loads(request.POST['data'])['callback']
            message_id = fields['apiMsgId']
            address = fields['to']
            status_code = fields['status']
            return message_id, address, Clickatell.STATUSES[status_code]
        except (ValueError, KeyError) as e:
            raise ClickatellException(str(e))

    def process_reply(self, request):
        '''
        Extracts and returns (message_id, address, text, datetime)
        from request.
        '''
        if request.method != "POST":
            raise ClickatellException("Invalid request type")
        try:
            fields = json.loads(request.POST['data'])['callback']
            assert fields['api_id'] == self.api_id
            message_id = fields['moMsgId']
            address = fields['from']
            charset = fields['charset']
            text = fields['text'].decode(charset)
            timestamp = datetime.strptime(fields['timestamp'], '%Y-%m-%d%H:%M:%S')
            # Clickatell documentation mentions using GMT +2
            timestamp = pytz.timezone("Africa/Johannesburg").localize(timestamp)
            return message_id, address, text, timestamp
        except (ValueError, KeyError) as e:
            raise ClickatellException(str(e))
        except AssertionError:
            raise ClickatellException("Reply message does not match API ID") 


def send_smses(api_name, numbers, message, enable_reply=False):
    '''
    Sends SMSes using the specified API (only Clickatell at the moment).
    Saves and returns [(SMS object), ...] for each SMS sent.
    '''
    api_obj = _get_api_obj(api_name)
    # sends SMSes and creates SMS objects
    results = api_obj.send(numbers, message, enable_reply)
    sms_objects = [SMS.objects.create(message_id=mid, mobile_number=msisdn)
                   for mid, msisdn in results]
    return sms_objects


def process_status_report(api_name, request):
    '''
    Processes an SMS delivery status report, updating the relevant
    SMS's delivery status.
    '''
    api_obj = _get_api_obj(api_name)
    message_id, mobile_number, status = api_obj.process_status_report(request)
    cutoff = timezone.now() - timedelta(hours=48)
    matched_smses = SMS.objects.filter(message_id=message_id,
                                       mobile_number=mobile_number,
                                       created__gte=cutoff)
    if len(matched_smses) == 0 or len(matched_smses) > 1:
        # don't update - either there is no matching sms or
        # the message_id and MSISDN don't refer to a unique
        # sms in the last 48 hours (highly unlikely but we are
        # not being restrictive in db model)
        return False
    matched_smses.update(delivery_status=status)
    return True


def process_reply(api_name, request):
    api_obj = _get_api_obj(api_name)
    message_id, mobile_number, text, timestamp = api_obj.process_reply(request)
    matched_smses = SMS.objects.filter(message_id=message_id,
                                       mobile_number=mobile_number) \
                               .order_by('-created')
    if len(matched_smses) == 0:
        return False
    # assume the reply is for the latest matching sms
    sms_reply_received.send(sender=api_obj,
                            instance=matched_smses[0],
                            text=text,
                            timestamp=timestamp)
    return True


def _get_api_obj(api_name):
    '''
    Instantiate and return an SMS API object. The API's settings
    dict is passed as keyword arguments to __init__.
    '''
    try:
        api_class = {
            'Clickatell': Clickatell
        }[api_name]
        api_kwargs = {
            'Clickatell': settings.CLICKATELL
        }[api_name]
        return api_class(**api_kwargs)
    except KeyError:
        raise InvalidAPIError(api_name)
    except AttributeError:
        raise ImproperlyConfigured("Settings for %s are missing" % api_name)
    except TypeError:
        raise ImproperlyConfigured("Invalid settings for %s" % api_name)
