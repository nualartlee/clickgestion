"""
Django settings for clickgestion project.

Generated by 'django-admin startproject' using Django 1.11.14.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# Get password from docker secrets
#print('Executing uid: {}'.format(os.geteuid()))
#print('Secret files: {}'.format(os.listdir('/run/secrets/')))
with open('/run/secrets/django_secret_key', 'r') as secret_file:
    DJANGO_SECRET_KEY = secret_file.read()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DJANGO_SECRET_KEY


ALLOWED_HOSTS = ['*']


# Crispy forms templates
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'debug_toolbar',
    'crispy_forms',
    'pure_pagination',
    'clickgestion.core',
    'clickgestion.transactions',
    'clickgestion.apt_rentals',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'clickgestion.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'clickgestion.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

# Get password from docker secrets
with open('/run/secrets/postgres_password', 'r') as secret_file:
    POSTGRES_PASS = secret_file.read()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'clickgestion',
        'USER': 'postgres',
        'PASSWORD': POSTGRES_PASS,
        'HOST': 'postgres',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
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

LOGIN_URL = '/login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

TIME_ZONE = 'Europe/Madrid'
#TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# django-pure-pagination settings
PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 8,
    'MARGIN_PAGES_DISPLAYED': 1,

    'SHOW_FIRST_PAGE_WHEN_INVALID': True,
}