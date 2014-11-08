"""
Django settings for questr project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

## SECRETS, ACCESS AND API KEYS
SECRET_KEY = os.environ['LOCAL_SECRET_KEY']

# Mandrill API KEY
MANDRILL_API_KEY = os.environ['MANDRILL_API_KEY']
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

# Amazon S3 Access Keys
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_ACCESS_KEY_ID = os.environ['AMAZON_ACCESS_KEY_ID']
AWS_S3_SECRET_ACCESS_KEY = os.environ['AMAZON_SECRET_ACCESS_KEY']
AWS_HEADERS = { 'Cache-Control' : 'max-age=86400',}
AWS_MEDIA_BUCKET = os.environ['AWS_MEDIA_BUCKET']
AWS_STATIC_BUCKET = os.environ['AWS_STATIC_BUCKET']

# Google Maps Keys
GOOGLE_SERVER_API_KEY = os.environ['GOOGLE_SERVER_API_KEY']
GOOGLE_BROWSER_API_KEY = os.environ['GOOGLE_BROWSER_API_KEY']

# DATABASE ENGINE CONFIGURATIONS
import dj_database_url
DATABASES = {
    "default": dj_database_url.config()
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# APPLICATION DEFINITIONS
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mailchimp',
    'users',
    'djrill',
    'quests',
    'south',
    'reviews',
    'storages',
    'endless_pagination',
    'djcelery',
)

# MIDDLERWARE DEFINITIONS
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# AUTH BACKEND DEFINITIONS
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    )

# TEMPLATE CONTEXT DEFINITIONS
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)

# TEMPLATE PATH CONFIGURATION 
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
TEMPLATE_DIRS = (TEMPLATE_PATH)

## MISCELLANEOUS SETTINGS

ROOT_URLCONF = 'questr.urls'
WSGI_APPLICATION = 'questr.wsgi.application'
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/Toronto'
USE_I18N = True
USE_L10N = True
USE_TZ = True
APPEND_SLASH = True

# TURN DEBUG OFF
DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['*']

# QUESTR HOMEPAGE URL
QUESTR_URL = os.environ['QUESTR_URL'] 

# QUESTR PROXIMITY
QUESTR_PROXIMITY = 11

# Static asset configuration
STATIC_URL = 'http://s3.amazonaws.com/%s/' % AWS_STATIC_BUCKET
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)

# CONFIGURING QUESTRUSERPROFILE AS THE AUTH BACKEND
AUTH_USER_MODEL = 'users.QuestrUserProfile'

# LOGIN URL DEFINITIONS
LOGIN_URL = '/user/signin/'
LOGIN_REDIRECT_URL = '/user/home/'

## LOGGING DEFINITION AND CONFIGURATION

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'users': {
            'handlers':['console'],
            'level':'DEBUG',
        },
        'quests': {
            'handlers':['console'],
            'level':'DEBUG',
        },
        'reviews': {
            'handlers':['console'],
            'level':'DEBUG',
        },
        'libs': {
            'handlers':['console'],
            'level':'DEBUG',
        },
    }
}

# CELERY DEFINITIONS
BROKER_URL = os.environ['CLOUDAMQP_URL']
BROKER_CONNECTION_TIMEOUT = int(os.environ['BROKER_CONNECTION_TIMEOUT'])
BROKER_CONNECTION_RETRY = int(os.environ['BROKER_CONNECTION_RETRY'])
BROKER_POOL_LIMIT = int(os.environ['BROKER_POOL_LIMIT'])
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'America/Toronto'
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_BEAT_SCHEDULER = 'djcelery.schedulers.DatabaseScheduler'
##BROKER POOL LIMIT CALC FMLA = BROKER_POOL_LIMIT * (gunicorn-workers * web dynos + worker dynos)

# QUESTR NOTIFICAITON INTERVALS
COURIER_ACTIVATION_INTERVAL = os.environ['COURIER_ACTIVATION_INTERVAL']
COURIER_SELECTION_DELAY = os.environ['COURIER_SELECTION_DELAY']
REJECTED_COURIER_HOLD_TIMER = os.environ['REJECTED_COURIER_HOLD_TIMER']
# LOCAL CONFIG IMPORT, IMPORTS ALL CONFIG FROM local_setting.py, required only for a dev env
try:
    from local_setting import *
except ImportError:
    pass

# Use amazon S3 storage only on production
if not DEBUG:
    ##This for media, user uploaded files
    DEFAULT_FILE_STORAGE = 'libs.s3utils.MediaRootS3BotoStorage'
    ##This for CSS,
    STATICFILES_STORAGE = 'libs.s3utils.StaticRootS3BotoStorage'
    MEDIA_ROOT = '/%s/' % DEFAULT_FILE_STORAGE
    MEDIA_URL = '//s3.amazonaws.com/%s/' % AWS_MEDIA_BUCKET


##DJANGO AVATAR SETTINGS
AVATAR_STORAGE_DIR = '/%s/media/' % DEFAULT_FILE_STORAGE
AVATAR_ALLOWED_FILE_EXTS = ('.jpg','.jpeg','.png')
AVATAR_MAX_SIZE = 125000000
AVATAR_THUMB_QUALITY = 85
AVATAR_THUMB_FORMAT = 'JPEG'

#TWILIO SETTINGS
TWILIO_ACCOUNT_SID=os.environ['TWILIO_ACCOUNT_SID']
TWILO_AUTH_TOKEN=os.environ['TWILO_AUTH_TOKEN']
TWILIO_NUM_1 = os.environ['TWILIO_NUM_1']