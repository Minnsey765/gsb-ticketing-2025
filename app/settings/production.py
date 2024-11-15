import os

from .common import *

ALLOWED_HOSTS = [
    'localhost',
    'ec2-13-51-72-40.eu-north-1.compute.amazonaws.com',
    '13.51.72.40',
]
DEBUG = True
SECRET_KEY = 'croissant'

# if 'SECRET_KEY' in os.environ:
# SECRET_KEY = os.environ["SECRET_KEY"]

# db


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gsb-data',
        'USER': os.environ["POSTGRES_USER"],
        'PASSWORD': 'man_in_a_box',
        'HOST': 'postgres',
        'PORT': '5432',
    }
}

MAX_CONN_AGE = 600
# STATIC_ROOT = BASE_DIR / "staticfiles"

# STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"


ADMINS = [
    ('Yuvraj', 'yuvraj@yuvrajdubey.co.uk'),
]


# AWS SES CONFIGURATION (i added "AWS_USER_ACCOUNT_ID = '864899874397'" but idk if it's meant to go here or if it's needed at all)
"""
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'eu-west-2'
AWS_SES_REGION_ENDPOINT = 'email-smtp.eu-west-2.amazonaws.com'
AWS_USER_ACCOUNT_ID = '864899874397'
USE_SES_V2 = True

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_SES_AUTO_THROTTLE = 0.8
"""

# SMTP CONFIGURATION
EMAIL_HOST = 'email-smtp.eu-west-2.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = f'it@girtonspringball.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""


# expire user sessions after 1 hour
SESSION_COOKIE_AGE = 60 * 60

STATIC_ROOT = 'static/'

STATIC_URL = 'static/'
