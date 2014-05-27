import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from sms.api import Clickatell, _get_api_obj
from sms.models import SMS


class ClickatellTestCase(TestCase):

    def test_err_response(self):
        # TODO: test for multi message response
        resp_text = 'ERR: 1235, This is an error message\n'
        match = Clickatell.ERROR_REGEX.match(resp_text)
        self.assertTrue(match)
        self.assertEqual(match.group('err_no'), '1235')
        self.assertEqual(match.group('err_description'),
                         'This is an error message')

    def test_send_response(self):
        # TODO: test for single message response
        resp_text = 'ID: 1e27304fb82b4cbd2bd21f0d883b8ada To: 27733416692\n' \
                    'ID: d49c1d82c01bf44c73273b168b3fce96 To: 27825052552\n'
        matches = Clickatell.SEND_REGEX.findall(resp_text)
        self.assertEqual(len(matches), 2)
        for groups, apimsgid, address in zip(matches,
                                             ['1e27304fb82b4cbd2bd21f0d883b8ada',
                                              'd49c1d82c01bf44c73273b168b3fce96'],
                                             ['27733416692', '27825052552']):
            self.assertEqual(groups[0], apimsgid)
            self.assertEqual(groups[2], address)

    def test_session_response(self):
        resp_text = 'OK: this_is_a_session_id\n'
        match = Clickatell.SESSION_REGEX.match(resp_text)
        self.assertTrue(match)
        self.assertEqual(match.group('session_id'), 'this_is_a_session_id')

    def test_process_status_report(self):
        factory = RequestFactory()
        payload = {'callback': {
            'apiMsgId': '996411ad91fa211e7d17bc873aa4a41d',
            'cliMsgId': '',
            'timestamp': 1218008129,
            'to': '279995631564',
            'from': '27833001171',
            'charge': 0.300000,
            'status': '004'
        }}
        request = factory.post('/status-callback/',
                               {'data': json.dumps(payload)})
        api_obj = _get_api_obj('Clickatell')
        result = api_obj.process_status_report(request)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], payload['callback']['apiMsgId'])
        self.assertEqual(result[1], payload['callback']['to'])
        self.assertEqual(result[2], Clickatell.STATUSES[payload['callback']['status']])


class ApiTestCase(TestCase):

    def test_process_status_report(self):
        payload = {'callback': {
            'apiMsgId': '996411ad91fa211e7d17bc873aa4a41d',
            'cliMsgId': '',
            'timestamp': 1218008129,
            'to': '279995631564',
            'from': '27833001171',
            'charge': 0.300000,
            'status': '004'
        }}
        sms_pk = SMS.objects.create(
            message_id=payload['callback']['apiMsgId'],
            mobile_number=payload['callback']['to'],
        ).pk
        data = {'data': json.dumps(payload)}
        valid_r = self.client.post(reverse('sms-status-callback'), data)
        get_r = self.client.get(reverse('sms-status-callback'), data)
        invalid_r = self.client.post(reverse('sms-status-callback'), {'data': '{]'})
        self.assertEqual(valid_r.status_code, 200)
        self.assertEqual(get_r.status_code, 405)
        # this test passes because Django forces DEBUG = False in tests
        self.assertEqual(invalid_r.status_code, 200)
        self.assertEqual(SMS.objects.get(pk=sms_pk).delivery_status,
                         Clickatell.STATUSES[payload['callback']['status']])
