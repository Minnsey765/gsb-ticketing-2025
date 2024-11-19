import os
import json
import boto3
from pathlib import Path

import dj_database_url

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'baguette'


DEBUG = True

# ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "scanner",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Here
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "scanner.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "scanner.wsgi.application"

MAX_CONN_AGE = 600



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

if (arn := os.environ.get("AWS_SECRET_ARN")):
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

# expire user sessions after 2 hours
SESSION_COOKIE_AGE = 60 * 60 * 2

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

ADMINS = [
    ('Matias', 'info@matiasilva.com'),
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_HOST = 'smtp.zeptomail.eu'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = f'it@girtonspringball.com'

if 'EMAIL_HOST_USER' in os.environ:
    EMAIL_HOST_PASSWORD = os.environ["EMAIL_HOST_PASSWORD"]
    EMAIL_HOST_USER = os.environ["EMAIL_HOST_USER"]
