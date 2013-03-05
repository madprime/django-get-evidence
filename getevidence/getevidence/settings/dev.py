"""Development settings and globals."""

from base import *


########## DEBUG CONFIGURATION
DEBUG = True
TEMPLATE_DEBUG = DEBUG


########## EMAIL CONFIGURATION
# Instead of sending real emails, write emails to stdout.
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', 
        'NAME': 'getevidence',                      
        'USER': 'getevidence',
        'PASSWORD': 'glassworks',
        'HOST': 'localhost',                      
        'PORT': '',                      
    }
}


########## GENERAL CONFIGURATION
TIME_ZONE = 'America/New_York'
