from .common import *

DEBUG = True
SECRET_KEY = 'croissant'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'gsb_db.db',
    }
}

STATIC_URL = 'static/'

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

EMAIL_HOST = 'email-smtp.eu-west-2.amazonaws.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
SERVER_EMAIL = f'it@girtonspringball.com'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST_PASSWORD = ""
EMAIL_HOST_USER = ""

#EMAIL_HOST = 'smtp.zoho.eu'
#EMAIL_PORT = 587
#EMAIL_USE_TLS = True
#SERVER_EMAIL = f'it@girtonspringball.com'

#EMAIL_HOST_PASSWORD = ""
#EMAIL_HOST_USER = "it@girtonspringball.com"

ADMINS = [
    ('Bob', 'bob@thebuilder.com'),
]
