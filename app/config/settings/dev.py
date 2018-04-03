from .base import *

DEBUG = True
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

WSGI_APPLICATION = 'config.wsgi.dev.application'

secrets = json.loads(open(SECRET_DEV, 'rt').read())

INSTALLED_APPS += [
    'django_extensions',
]


set_config(secrets, module_name=__name__, start=True)






