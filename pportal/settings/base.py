"""
Django settings for pportal project.

Generated by 'django-admin startproject' using Django 1.11.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os,sys
from .acessorio import *
from django.core.exceptions import ImproperlyConfigured
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))
#
#sys.path.append(OTHERS)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f=zue$c!65h^ycp0byej*!rw-6%xa#3!+*7!yv&(f1ebqzgjpa'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



#DEFAULT_FROM_EMAIL = 'noreply VIB proteomics<noreply-prc@vib-ugent.be>' #'noreply-prc@vib-ugent.be'
#DEFAULT_FROM_EMAIL = 'teresa.maia@vib-ugent.be' #'noreply-prc@vib-ugent.be'
#ADMINS = (
#    ('T Maia', 'teresa.maia@vib-ugent.be'))

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'requests',
    'bootstrap4',
    'crispy_forms',
    'formtools',
    'multiselectfield',
]


#AUTH_PROFILE_MODEL = 'requests.User'
AUTH_USER_MODEL = 'requests.User'
#AUTH_USER_MODEL = 'requests.User' # changes build in user model to this one
LOGIN_URL='login'
LOGIN_REDIRECT_URL='home'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pportal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
        ],

        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pportal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Brussels'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
#from .acessorio import * 
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, "static-dev"),
]
#STATIC_ROOT = [os.path.join(os.path.dirnameBASE_DIR), "static-dev"),
#]
#os.path.join(os.path.join(os.path.dirname(BASE_DIR), "pportal3"),"templates")]

CRISPY_TEMPLATE_PACK='bootstrap4'
MEDIA_ROOT = os.path.join(BASE_DIR, "media").replace('\\','/')
MEDIA_URL = "/media/"

# gmail settings
# # vibmail.ugent.be settings
# EMAIL_HOST = 'vibmail.ugent.be'
# EMAIL_HOST_USER = 'teresa.maia@vib-ugent.be'
# EMAIL_HOST_PASSWORD = 'Pin.tal1'
# EMAIL_PORT = 25
# EMAIL_USE_TLS = False


# #DEFAULT_FROM_EMAIL = 'noreply VIB proteomics<noreply-prc@vib-ugent.be>' #'noreply-prc@vib-ugent.be'
# DEFAULT_FROM_EMAIL = 'teresa.maia@vib-ugent.be' #'noreply-prc@vib-ugent.be'
# ADMINS = (
#     ('T Maia', 'teresa.maia@vib-ugent.be'))
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

#DEFAULT_FROM_EMAIL = 'noreply VIB proteomics<noreply-prc@vib-ugent.be>' #'noreply-prc@vib-ugent.be'
#DEFAULT_FROM_EMAIL = 'mtpmmaia@gmail.com' #'noreply-prc@vib-ugent.be'

#ADMINS = (
#    ('Te M', 'mtpmmaia@gmail.com'))
# gmail settings

def get_env_variable(name):
    """Gets the environment variable or throuws ImproperlyConfigured exceptions
    :rtype: object
    """
    try:
        return os.environ[name]
    except KeyError:
        raise ImproperlyConfigured(
            'Environment variable "%s" not found.' % name)

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'mtpmmaia@gmail.com'
from .emacessorio import *
#try:
#    import acessorio
#except ImportError:
#    EMAIL_HOST_PASSWORD = 'mtppmaia'
#else:
EMAIL_HOST_PASSWORD = EM_PW
EMAIL_PORT = 587
EMAIL_USE_TLS = True
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # during development only
DEFAULT_FROM_EMAIL = 'mtpmmaia@gmail.com>' #'noreply-prc@vib-ugent.be'
ADMINS = (
    ('Te M', 'mtpmmaia@gmail.com'))
MANAGERS = ADMINS