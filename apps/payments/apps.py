__author__ = 'freddie'

from django.apps import AppConfig


class MyAppConfig(AppConfig):
    name = 'payments'
    verbose_name = 'Payments'

    def ready(self):
        import signals.receivers
