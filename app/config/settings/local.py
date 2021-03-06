from .base import *

DEBUG = True
ALLOWED_HOSTS = []

WSGI_APPLICATION = 'config.wsgi.local.application'
INSTALLED_APPS += [
    'django_extensions',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}



