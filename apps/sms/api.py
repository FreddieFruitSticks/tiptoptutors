import requests


class SMSApi(object):
    '''
    Base class for integrating with 3rd-party SMS service.
    '''

    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url

    def send(self, numbers, messages):
        raise NotImplementedError

    def get_responses(self):
        raise NotImplementedError


