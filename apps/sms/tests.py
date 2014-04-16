from django.test import TestCase

from sms.api import Clickatell


class ClickatellTestCase(TestCase):

    def test_err_response(self):
        resp_text = 'ERR: 1235, This is an error message\n'
        match = Clickatell.ERROR_REGEX.match(resp_text)
        self.assertTrue(match)
        self.assertEqual(match.group('err_no'), '1235')
        self.assertEqual(match.group('err_description'),
                         'This is an error message')

    def test_send_response(self):
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
