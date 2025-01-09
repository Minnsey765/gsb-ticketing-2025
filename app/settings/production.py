import json
import os

import boto3

from .common import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gsb-data',
        'USER': 'gsb-ticketing',
        'PASSWORD': 'man_in_a_box',  #'man_in_a_box',
        'HOST': 'postgres',  #'postgres',
        'PORT': '5432',  #'5432',
    }
}

if arn := os.environ.get("AWS_SECRET_ARN"):
    client = boto3.client('secretsmanager')

    secret = client.get_secret_value(SecretId=arn).get('SecretString')

    creds = json.loads(secret)

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'postgres',
            'USER': creds['username'],
            'PASSWORD': creds['password'],  #'man_in_a_box',
            'HOST': creds['host'],  #'postgres',
            'PORT': creds['port'],  #'5432',
        }
    }


ALLOWED_HOSTS = [
    'localhost',
    'eewmuefw2h.execute-api.eu-west-2.amazonaws.com',
    'ticketing.girtonspringball.com',
    '13.51.72.40',
]
DEBUG = True
SECRET_KEY = 'croissant'

# if 'SECRET_KEY' in os.environ:
# SECRET_KEY = os.environ["SECRET_KEY"]

# db


MAX_CONN_AGE = 600
# STATIC_ROOT = BASE_DIR / "staticfiles"


ADMINS = [
    ('Yuvraj', 'yuvraj@yuvrajdubey.co.uk'),
    ('Oliver', 'om380@cam.ac.uk'),
]


"""
EMAIL_BACKEND = 'django_ses.SESBackend'
AWS_SES_REGION_NAME = 'eu-west-2'
AWS_SES_REGION_ENDPOINT = 'email-smtp.eu-west-2.amazonaws.com'
USE_SES_V2 = True


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

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}
