from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'lang',
        'USER': 'lang',
        'PASSWORD': 'test123',
        'HOST': 'database',
        'PORT': '5432',
    },
}
