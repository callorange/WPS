from .base import *

DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.elasticbeanstalk.com',
]

WSGI_APPLICATION = 'config.wsgi.dev.application'

INSTALLED_APPS += [
    'django_extensions',
    'storages',
]

DEFAULT_FILE_STORAGE = 'config.storage.DefaultFilesStorage'
# STATICFILES_STORAGE = 'config.storage.StaticFilesStorage'

secrets = json.loads(open(SECRET_DEV, 'rt').read())
set_config(secrets, module_name=__name__, start=True)
