import os.path
import sys
import site

# SECRET_KEY = 'sdafas88d*&ASD98asda897sda*&(*!@)*&^@'
sys.path.append(os.path.join(os.path.dirname(__file__), 'apps'))

# ==============================================================================
# django
# ==============================================================================

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = PROJECT_ROOT

USE_DJANGO_JQUERY = False

PROJECT_FOLDER = 'tiptoptutors'
PROJECT_NAME = 'tiptoptutors'
PROJECT_DOMAIN = "tiptoptutors.co.za"

SITE_DOMAIN = "https://%s" % PROJECT_DOMAIN

ROOT_URLCONF = "urls"

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATETIME_FORMAT = "d/m/Y H:i:s"
DATE_FORMAT = "d/m/Y"

# ==============================================================================
# database settings
# ==============================================================================

# For Postgres (not location aware) do from command line
# echo "CREATE USER skeleton WITH PASSWORD 'skeleton'" | sudo -u postgres psql
# echo "CREATE DATABASE skeleton WITH OWNER skeleton ENCODING 'UTF8'" | sudo -u postgres psql

# For MySQL remember to first do from a MySQL shell:
# CREATE database skeleton;
# GRANT ALL ON skeleton.* TO 'skeleton'@'localhost' IDENTIFIED BY 'skeleton';
# GRANT ALL ON test_skeleton.* TO 'skeleton'@'localhost' IDENTIFIED BY 'skeleton';
# FLUSH PRIVILEGES;

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'tiptoptutors',
        'USER': 'tiptoptutors',
        'PASSWORD': 'tiptoptutors',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# ==============================================================================
# mail settings
# ==============================================================================

ADMINS = (
    ('darren', 'darren@symfony.co.za'),
    ('freddie', 'info@tiptoptutors.co.za'),
    ('riz', 'rizziepit@gmail.com')
)
MANAGERS = ADMINS

# web contact form
'''
TEST_EMAIL_DIR = os.path.join(os.path.dirname(__file__), 'tmp', 'test_emails')
WEBCONTACT_RECIPIENTS = (
    'info@tiptoptutors.co.za',
)
EMAIL_TEST_MAIL = True
EMAIL_SYSTEM_SENDER = "%s <no-reply@%s>" % (PROJECT_NAME, PROJECT_DOMAIN)
MAIL_WRITE_TO_HDD = False
'''

# Django email settings
DEFAULT_FROM_EMAIL = "no-reply@tiptoptutors.co.za"
SERVER_EMAIL = 'server@tiptoptutors.co.za'
# Note: Google has 99 emails per day limit
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = '0f6GjAAponwMy4XqCeAh'
EMAIL_HOST_USER = 'no-reply@tiptoptutors.co.za'


# ==============================================================================
# project settings
# ==============================================================================

LOGIN_URL = "/admin/"

TIME_ZONE = 'Africa/Johannesburg'
LANGUAGE_CODE = 'en_uk'

SECRET_KEY = 'zi@=&o6gf&5g4g7%s4wxcr!^z$d!o$3#s_u7)mp9qa)$p7^&in'

SITE_ID = 1
USE_L10N = False
USE_I18N = False
USE_TZ = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'
# STATIC_ROOT = os.path.join(PROJECT_ROOT,"static")
STATIC_ROOT = "/static/"
STATIC_URL = '/static/'

# need to comment this out for prod and dev servers. I think it has something to do with how static files are served
# using "runserver" locally versus how whitenoise runs it on dev.
STATICFILES_DIRS = (PROJECT_DIR + '/static/',)
# comment this out for production site - this is only for testing.
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/app-messages'

ADMIN_TOOLS_MEDIA_URL = ''
ADMIN_MEDIA_PREFIX = '/static/admin/'

AUTH_USER_MODEL = 'customuser.CustomAuthUser'

INTERNAL_IPS = ('127.0.0.1',)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',

)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MIDDLEWARE_CLASSES = (
    'djangosecure.middleware.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

DJANGO_CONTRIB_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.humanize',
    'django.contrib.webdesign',

)

PROJECT_APPS = (
    'tutor',
    'pupil',
    'sms',
    'option',
    'common',
    'blog',
    'contact',
    'quote',
    'matchmaker',
    'tutor_login',
    'payments',
    'customuser',
    # 'django_custom_user_migration',
    'password_reset',
    'sslserver',
    # 'djangosecure',
)

THIRD_PARTY_APPS = (
    'debug_toolbar',
    'djcelery',
    'kombu.transport.django'

)

INSTALLED_APPS = DJANGO_CONTRIB_APPS + PROJECT_APPS + THIRD_PARTY_APPS

DEBUG_TOOLBAR_PATCH_SETTINGS = False

# ==============================================================================
# Celery configuration
# ==============================================================================

BROKER_URL = "django://"
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'

# ==============================================================================
# SMS configuration
# ==============================================================================

CLICKATELL = {
    'username': 'tiptoptutors',
    'password': '3aHaLfh09Ac3gcPbeTsT',
    'endpoint_url': 'http://api.clickatell.com/http',
    'api_id': '3478778',
    'sender_id': '36000',  # a short code that has been approved and configured for the api_id
}

BULKSMS = {
    'username': 'tiptoptutors',
    'password': 'MPKoBAbFhncL6QXWrANh',
    'endpoint_url': 'http://bulksms.2way.co.za:5567/eapi',
    'push_password': '4v15tv087nfl34ucn'
}
# ==============================================================================
# Template directories
# ==============================================================================

TEMPLATE_DIRS = (os.path.join(PROJECT_DIR, 'templates'),)

for app in PROJECT_APPS:
    if os.path.isdir(os.path.join(PROJECT_DIR, app, 'templates')):
        TEMPLATE_DIRS += (os.path.join(PROJECT_DIR, app, 'templates'),)

    if os.path.isdir(os.path.join(PROJECT_DIR, app, 'templates/partials')):
        TEMPLATE_DIRS += (os.path.join(PROJECT_DIR, app, 'templates/partials'),)

    if os.path.isdir(os.path.join(PROJECT_DIR, app, 'templates/text')):
        TEMPLATE_DIRS += (os.path.join(PROJECT_DIR, app, 'templates/text'),)


# ==============================================================================
# Logging
# ==============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
}

# ==============================================================================
#  overrides settings
# ==============================================================================

try:
    from settings_local import *

    print "import settings local"
except ImportError:
    pass
