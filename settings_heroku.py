import os

import dj_database_url

from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES['default'] = dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure(). These are all security settings to ensure sending over
# https instead of http.
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = False

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
# STATICFILES_DIRS = (
#     os.path.join(PROJECT_ROOT, 'static'),
# )

INSTALLED_APPS += ('gunicorn',)
