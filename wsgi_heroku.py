"""
WSGI config for tiptoptutors project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings_heroku")

# newrelic setup
import newrelic.agent
os.environ.setdefault("NEW_RELIC_CONFIG_FILE", "newrelic.ini")
newrelic.agent.initialize(os.environ["NEW_RELIC_CONFIG_FILE"])

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

application = get_wsgi_application()
application = DjangoWhiteNoise(application)