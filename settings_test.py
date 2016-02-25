from settings import *


# faster for testing
DATABASES['default'].update({
    'ENGINE': 'django.db.backends.sqlite3',
    'USER': '',
    'PASSWORD': '',
})
