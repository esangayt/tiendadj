from .base import *
import firebase_admin
from firebase_admin import credentials, auth

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5431',
    }
}

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'utils.ManagerResponse.custom_exception_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'utils.CustomJSONRenderer.CustomJSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ]
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR.child('static')]

# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR.child('media')

cred = credentials.Certificate('django-key.json')
default_app = firebase_admin.initialize_app(cred)

