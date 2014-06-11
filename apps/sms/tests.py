import json, pytz
from datetime import datetime
from urllib import urlencode

from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import RequestFactory

from sms.api import (Clickatell, BulkSMS, _get_api_obj, sms_reply_received,
                     BulkSMSException)
from sms.models import SMS

from mock import create_autospec


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
        self.assertEqual(result[0], Clickatell.get_message_id(payload['callback']['apiMsgId']))
        self.assertEqual(result[1], payload['callback']['to'])
        self.assertEqual(result[2], Clickatell.STATUSES[payload['callback']['status']])

    def test_process_reply(self):
        factory = RequestFactory()
        payload = {'callback': {
            'moMsgId': 'b2aee337abd962489b123fda9c3480fa',
            'timestamp': '2008-08-0609:43:50',
            'to': '279995631564',
            'from': '27833001171',
            'text': 'Hereisthe messagetext',
            'api_id': '3478778',
            'charset': 'ISO-8859-1',
            'udh': '',
        }}
        request = factory.post('/reply-callback/',
                               {'data': json.dumps(payload)})
        api_obj = _get_api_obj('Clickatell')
        result = api_obj.process_reply(request)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], Clickatell.get_message_id(payload['callback']['moMsgId']))
        self.assertEqual(result[1], payload['callback']['from'])
        self.assertEqual(result[2], payload['callback']['text']\
                                    .decode(payload['callback']['charset']))
        timestamp = datetime(year=2008, month=8, day=6,
                             hour=7, minute=43, second=50,
                             tzinfo=pytz.utc)
        self.assertEqual(result[3], timestamp)


class BulkSMSTestCase(TestCase):

    def test_err_response(self):
        resp_text = '23|invalid credentials (username was: john)|'
        match = BulkSMS.ERROR_REGEX.match(resp_text)
        self.assertTrue(match)
        self.assertEqual(match.group('status_code'), '23')
        self.assertEqual(match.group('status_description'),
                         'invalid credentials (username was: john)')

    def test_send_response(self):
        for resp_text in ('0|success|1234', '0|success|1234\n', '0|success|1234 '):
            match = BulkSMS.SEND_REGEX.match(resp_text)
            self.assertTrue(match)
            self.assertEqual(match.group('status_code'), '0')
            self.assertEqual(match.group('status_description'), 'success')
            self.assertEqual(match.group('batch_id'), '1234')
            self.assertFalse(BulkSMS.ERROR_REGEX.match(resp_text))

    def test_process_status_report(self):
        factory = RequestFactory()
        payload = {
            'batch_id': '12345',
            'completed_time': '14-05-25 12:05:11',
            'msisdn': '27833001171',
            'status': '11',
            'unique_id': '1',
            'source_id': '',
            'pass': settings.BULKSMS['push_password']
        }
        request = factory.get('/status-callback/?%s' % urlencode(payload))
        api_obj = _get_api_obj('BulkSMS')
        result = api_obj.process_status_report(request)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], BulkSMS.get_message_id(payload['batch_id']))
        self.assertEqual(result[1], payload['msisdn'])
        self.assertEqual(result[2], BulkSMS.STATUSES[payload['status']])

    def test_process_reply(self):
        factory = RequestFactory()
        payload = {
            'msisdn': '279995631564',
            'sender': '27833001171',
            'message': 'Hereisthe messagetext',
            'dca': '7bit',
            'msg_id': '111',  # same function as unique_id
            'source_id': '',
            'referring_batch_id': '12345',
            'network_id': '',
            # reply messages should never be more than 1 sms long
            # only the first message in the sequence should be processed
            'concat_reference': '',
            'concat_num_segments': '',
            'concat_seq_num': '',
            'received_time': '14-05-25 12:40:06',
            'pass': settings.BULKSMS['push_password']
        }
        request = factory.get('/reply-callback/?%s' % urlencode(payload))
        api_obj = _get_api_obj('BulkSMS')
        result = api_obj.process_reply(request)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], BulkSMS.get_message_id(payload['referring_batch_id']))
        self.assertEqual(result[1], payload['sender'])
        self.assertEqual(result[2], payload['message'])
        timestamp = datetime(year=2014, month=5, day=25,
                             hour=10, minute=40, second=6,
                             tzinfo=pytz.utc)
        self.assertEqual(result[3], timestamp)
        # test for 8bit and 16bit (badly)
        payload['dca'] = '8bit'
        payload['message'] = 'Hereisthe messagetext'.encode('hex')
        request = factory.get('/reply-callback/?%s' % urlencode(payload))
        self.assertEqual(api_obj.process_reply(request)[2], 'Hereisthe messagetext')
        payload['dca'] = '16bit'
        payload['message'] = 'Hereisthe messagetext'.encode('utf-16').encode('hex')
        request = factory.get('/reply-callback/?%s' % urlencode(payload))
        self.assertEqual(api_obj.process_reply(request)[2], 'Hereisthe messagetext')
        # test for failure
        payload['concat_seq_num'] = '2'
        request = factory.get('/reply-callback/?%s' % urlencode(payload))
        with self.assertRaises(BulkSMSException):
            api_obj.process_reply(request)


def signal_handler(sender, **kwargs):
    pass
reply_handler = create_autospec(signal_handler)


class ApiTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        sms_reply_received.connect(reply_handler, weak=False)

    @classmethod
    def tearDownClass(cls):
        sms_reply_received.disconnect(reply_handler)

    def tearDown(self):
        reply_handler.reset_mock()

    def test_process_status_report_clickatell(self):
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
            message_id=Clickatell.get_message_id(payload['callback']['apiMsgId']),
            mobile_number=payload['callback']['to'],
        ).pk
        data = {'data': json.dumps(payload)}
        valid_r = self.client.post(reverse('sms-status-callback'), data)
        self.assertEqual(valid_r.status_code, 200)
        self.assertEqual(SMS.objects.get(pk=sms_pk).delivery_status,
                         Clickatell.STATUSES[payload['callback']['status']])
        # check that invalid requests return appropriate response code
        get_r = self.client.get(reverse('sms-status-callback'), data)
        invalid_r = self.client.post(reverse('sms-status-callback'), {'data': '{]'})
        self.assertEqual(get_r.status_code, 200)
        # this test passes because Django forces DEBUG = False in tests
        self.assertEqual(invalid_r.status_code, 200)

    def test_process_reply_clickatell(self):
        payload = {'callback': {
            'moMsgId': 'b2aee337abd962489b123fda9c3480fa',
            'timestamp': '2008-08-0609:43:50',
            'to': '279995631564',
            'from': '27833001171',
            'text': 'Hereisthe messagetext',
            'api_id': '3478778',
            'charset': 'ISO-8859-1',
            'udh': '',
        }}
        sms = SMS.objects.create(
            message_id=Clickatell.get_message_id(payload['callback']['moMsgId']),
            mobile_number=payload['callback']['from'],
        )
        data = {'data': json.dumps(payload)}
        valid_r = self.client.post(reverse('sms-reply-callback'), data)
        self.assertEqual(valid_r.status_code, 200)
        timestamp = datetime(year=2008, month=8, day=6,
                             hour=7, minute=43, second=50,
                             tzinfo=pytz.utc)
        reply_handler.assert_called_with(signal=sms_reply_received,
                                         sender=_get_api_obj('Clickatell'),
                                         instance=sms,
                                         text=payload['callback']['text'],
                                         timestamp=timestamp)
        # check that invalid requests return appropriate response code
        get_r = self.client.get(reverse('sms-reply-callback'), data)
        invalid_r = self.client.post(reverse('sms-reply-callback'), {'data': '{]'})
        self.assertEqual(get_r.status_code, 200)
        # this test passes because Django forces DEBUG = False in tests
        self.assertEqual(invalid_r.status_code, 200)

    def test_process_status_report_bulksms(self):
        payload = {
            'batch_id': '12345',
            'completed_time': '14-05-25 12:05:11',
            'msisdn': '27833001171',
            'status': '11',
            'unique_id': '1',
            'source_id': '',
            'pass': settings.BULKSMS['push_password']
        }
        sms_pk = SMS.objects.create(
            message_id=BulkSMS.get_message_id(payload['batch_id']),
            mobile_number=payload['msisdn'],
        ).pk
        valid_r = self.client.get('%s?%s' % (reverse('sms-status-callback'),
                                             urlencode(payload)))
        self.assertEqual(valid_r.status_code, 200)
        self.assertEqual(SMS.objects.get(pk=sms_pk).delivery_status,
                         BulkSMS.STATUSES[payload['status']])
        # check that invalid requests return appropriate response code
        post_r = self.client.post(reverse('sms-status-callback'), payload)
        invalid_r = self.client.get(reverse('sms-status-callback'))
        self.assertEqual(post_r.status_code, 200)
        # this test passes because Django forces DEBUG = False in tests
        self.assertEqual(invalid_r.status_code, 200)

    def test_process_reply_bulksms(self):
        payload = {
            'msisdn': '279995631564',
            'sender': '27833001171',
            'message': 'Hereisthe messagetext',
            'dca': '7bit',
            'msg_id': '111',  # same function as unique_id
            'source_id': '',
            'referring_batch_id': '12345',
            'network_id': '',
            'concat_reference': '',
            'concat_num_segments': '',
            'concat_seq_num': '',
            'received_time': '14-05-25 12:40:06',
            'pass': settings.BULKSMS['push_password']
        }
        sms = SMS.objects.create(
            message_id=BulkSMS.get_message_id(payload['referring_batch_id']),
            mobile_number=payload['sender'],
        )
        valid_r = self.client.get('%s?%s' % (reverse('sms-reply-callback'),
                                             urlencode(payload)))
        self.assertEqual(valid_r.status_code, 200)
        timestamp = datetime(year=2014, month=5, day=25,
                             hour=10, minute=40, second=6,
                             tzinfo=pytz.utc)
        reply_handler.assert_called_with(signal=sms_reply_received,
                                         sender=_get_api_obj('BulkSMS'),
                                         instance=sms,
                                         text=payload['message'],
                                         timestamp=timestamp)
        # check that invalid requests return appropriate response code
        post_r = self.client.post(reverse('sms-reply-callback'), payload)
        invalid_r = self.client.get(reverse('sms-reply-callback'))
        self.assertEqual(post_r.status_code, 200)
        # this test passes because Django forces DEBUG = False in tests
        self.assertEqual(invalid_r.status_code, 200)
