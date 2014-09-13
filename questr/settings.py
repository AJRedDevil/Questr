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


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['LOCAL_SECRET_KEY']
SOCIAL_AUTH_FACEBOOK_KEY = os.environ['SOCIAL_AUTH_FACEBOOK_KEY']
SOCIAL_AUTH_FACEBOOK_SECRET = os.environ['SOCIAL_AUTH_FACEBOOK_SECRET']
SOCIAL_AUTH_TWITTER_KEY = os.environ['SOCIAL_AUTH_TWITTER_KEY']
SOCIAL_AUTH_TWITTER_SECRET = os.environ['SOCIAL_AUTH_TWITTER_SECRET'] 
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_KEY']
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = os.environ['SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET'] 
# Mandrill API Key
MANDRILL_API_KEY = os.environ['MANDRILL_API_KEY']
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"
# Amazon S3 Access Keys
AWS_S3_SECURE_URLS = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_ACCESS_KEY_ID = os.environ['AMAZON_ACCESS_KEY_ID']
AWS_S3_SECRET_ACCESS_KEY = os.environ['AMAZON_SECRET_ACCESS_KEY']
# AWS_STORAGE_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
AWS_MEDIA_BUCKET = os.environ['AWS_MEDIA_BUCKET']
AWS_STATIC_BUCKET = os.environ['AWS_STATIC_BUCKET']

# Google maps
GOOGLE_MAPS_SERVER_KEY = os.environ['GOOGLE_MAPS_SERVER_KEY']
GOOGLE_MAPS_BROWSER_KEY = os.environ['GOOGLE_MAPS_BROWSER_KEY']

#Append Slash to all cals
APPEND_SLASH = True
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

# ALLOWED_HOSTS = ['.questr.co']
ALLOWED_HOSTS = ['*']

DATABASES = {
"default": {
   "ENGINE": "django.db.backends.postgresql_psycopg2",
    }
}
#Database Settings for heroku
import dj_database_url
DATABASES['default'] =  dj_database_url.config()


# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Application definition
import mailchimp

INSTALLED_APPS = (
    # 'django.contrib.admin',
    # 'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'social.apps.django_app.default',
    'endless_pagination',
    'mailchimp',
    'users',
    'djrill',
    'quests',
    'south',
    'reviews',
    'storages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'questr.urls'

WSGI_APPLICATION = 'questr.wsgi.application'
# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Toronto'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Questr Url
QUESTR_URL = os.environ['QUESTR_URL'] 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
# Static asset configuration
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = 'http://s3.amazonaws.com/%s/' % AWS_STATIC_BUCKET
# MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')
# MEDIA_URL = '/questr-media/'
STATICFILES_DIRS = (
    os.path.join(PROJECT_PATH, 'static'),
)
# Add our own UserProfile as the backend auth module
AUTH_USER_MODEL = 'users.QuestrUserProfile'


# For Social Network Authentication
# User Model
# LOGIN_URL = '/user/login/'
# # LOGIN_ERROR_URL = '/user/login/'
# LOGIN_REDIRECT_URL = '/user/home/'
# SOCIAL_AUTH_LOGIN_ERROR_URL = '/'
# SOCIAL_AUTH_USERNAME_IS_FULL_EMAIL = True
# SOCIAL_AUTH_USER_MODEL = 'users.QuestrUserProfile'
# SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['email','first_name','last_name','displayname', 'username']
# SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
# SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['profile', 'email']
# SOCIAL_AUTH_PIPELINE = (
#         'social.pipeline.social_auth.social_details',
#         'social.pipeline.social_auth.social_uid',
#         'social.pipeline.social_auth.auth_allowed',
#         'social.pipeline.social_auth.social_user',
#         'social.pipeline.user.get_username',
#         'users.pipeline.required_fields',
#         'users.pipeline.create_user',
#         'users.pipeline.save_profile_picture',
#         'social.pipeline.mail.mail_validation',
#         'social.pipeline.social_auth.associate_user',
#         'social.pipeline.social_auth.load_extra_data',
#         'social.pipeline.user.user_details'
#     )

# Auth Backend
AUTHENTICATION_BACKENDS = (
    # 'social.backends.facebook.FacebookOAuth2',
    # 'social.backends.twitter.TwitterOAuth',
    # 'social.backends.google.GooglePlusAuth', # commented to disable google plus auth
    # 'social.backends.google.GoogleOAuth2',
    'django.contrib.auth.backends.ModelBackend',
    )

#Template context processors for social auth
TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)
TEMPLATE_PATH = os.path.join(PROJECT_PATH, 'templates')
TEMPLATE_DIRS = (TEMPLATE_PATH)

# All local configurations in local_setting
try:
    from local_setting import *
except ImportError:
    pass

# Use amazon S3 storage only on production
if not DEBUG:
    ##Use Amazon S3 as default storage
    ##This for media
    DEFAULT_FILE_STORAGE = 'libs.s3utils.MediaRootS3BotoStorage'
    ##This for CSS
    STATICFILES_STORAGE = 'libs.s3utils.StaticRootS3BotoStorage'
    MEDIA_ROOT = '/%s/' % DEFAULT_FILE_STORAGE
    MEDIA_URL = '//s3.amazonaws.com/%s/' % AWS_MEDIA_BUCKET

## Setup Logging ##

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
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'questr.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
    }
}