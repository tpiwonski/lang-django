from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('LANG_DB_NAME'),
        'USER': 'lang',
        'PASSWORD': 'test123',
        'HOST': 'database',
        'PORT': '5432',
    },
}
