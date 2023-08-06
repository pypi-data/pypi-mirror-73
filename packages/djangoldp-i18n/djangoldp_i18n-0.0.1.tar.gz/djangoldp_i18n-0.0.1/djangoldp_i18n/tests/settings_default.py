
from djangoldp.tests.settings_default import *

DJANGOLDP_PACKAGES=['djangoldp.tests', 'djangoldp_i18n.tests']
INSTALLED_APPS=('django.contrib.auth',
                'django.contrib.contenttypes',
                'django.contrib.sessions',
                'django.contrib.admin',
                'guardian',
                'djangoldp',
                'djangoldp.tests',
                'djangoldp_i18n.tests')

AUTH_USER_MODEL='tests.User'
