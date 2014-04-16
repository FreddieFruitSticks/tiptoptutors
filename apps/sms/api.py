import re
import time

from django.conf import settings

import requests


class SMSApi(object):
    '''
    Base class for integrating with 3rd-party SMS service.
    '''

    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url

    def send(self, numbers, message):
        raise NotImplementedError

    def get_responses(self):
        raise NotImplementedError


class ClickatellException(Exception):
    pass


class Clickatell(SMSApi):

    SESSION_TIMEOUT = 10 * 60  # Clickatell docs say 15 minutes
    ERROR_REGEX = re.compile(r'ERR:\s*(?P<err_no>\d+),\s*(?P<err_description>.*)')
    SESSION_REGEX = re.compile(r'OK:\s*(?P<session_id>.*)')
    SEND_REGEX = re.compile(r'ID:\s*(?P<apimsgid>\w+)(\s*To:\s*(?P<address>[0-9+]+))?[\s\n\r]*')

    def __init__(self, endpoint_url, api_id, username, password):
        self.endpoint_url = endpoint_url
        self.api_id = api_id
        self.username = username
        self.password = password
        self.session_id = None

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

    def send(self, numbers, message):
        '''
        Returns [(apimsgid, address), ...] for each number provided.
        Raises ClickatellException if a request fails.
        Note: Clickatell requires numbers in international format without
        the leading '+'.
        '''
        addresses = ','.join(numbers)
        params = {
            'to': addresses,
            'text': message
        }
        body = self._request('sendmsg', params)
        matches = Clickatell.SEND_REGEX.findall(body)
        return [(g[0], g[2]) for g in matches]
