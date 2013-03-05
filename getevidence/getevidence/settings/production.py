"""Development settings and globals."""

from base import *


########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        # 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'ENGINE': 'django.db.backends.sqlite3',

        # Name of database, or path to database file if using sqlite3.
        'NAME': 'getevidence',                      

        # The following settings are not used with sqlite3:
        'USER': 'getevidence',
        'PASSWORD': 'glassworks',
        'HOST': 'localhost',                      

        # Empty for localhost through domain sockets or '127.0.0.1' 
        # for localhost through TCP. Set to empty string for default.
        'PORT': '',                      
    }
}


########## GENERAL CONFIGURATION
TIME_ZONE = 'America/New_York'
