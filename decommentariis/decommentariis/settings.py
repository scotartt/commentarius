"""
Django settings for decommentariis project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '3f*@sdc0#4+t69hozq%iy^-vv(nyua$03zq#c!s69(hdkq5$qn'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

CACHES = {
	'default': {
		'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
	}
}

TEMPLATE_LOADERS = (
	'django.template.loaders.app_directories.Loader',
	'django.template.loaders.filesystem.Loader',
	)

TEMPLATE_DEBUG = True

SITE_ID=1

ALLOWED_HOSTS = [
]

# LOGIN_URL='/login/'

LOGIN_REDIRECT_URL='/' ## default redirect after success login if no "next"

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.sites',
	'decommentariis',
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	# 'allauth.socialaccount.providers.dropbox',
	#'allauth.socialaccount.providers.facebook',
	# 'allauth.socialaccount.providers.github',
	'allauth.socialaccount.providers.google',
	# 'allauth.socialaccount.providers.instagram',
	# 'allauth.socialaccount.providers.openid',
	'allauth.socialaccount.providers.twitter',
	'tastypie',
	)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	)
TEMPLATE_CONTEXT_PROCESSORS = (
	"django.core.context_processors.request",
	"django.contrib.auth.context_processors.auth",
	"allauth.account.context_processors.account",
	"allauth.socialaccount.context_processors.socialaccount",
	)
AUTHENTICATION_BACKENDS = (
	# Needed to login by username in Django admin, regardless of `allauth`
	"django.contrib.auth.backends.ModelBackend",
	# `allauth` specific authentication methods, such as login by e-mail
	"allauth.account.auth_backends.AuthenticationBackend",
	)

ROOT_URLCONF = 'decommentariis.urls'

WSGI_APPLICATION = 'decommentariis.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
'default': {
'ENGINE': 'django.db.backends.sqlite3',
'NAME': os.path.join(BASE_DIR, 'decommentariis_db.sqlite3'),
}
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/static/'

try:
	from decommentariis.prod_settings import *
except ImportError as e:
	print("Error importing prod settings: {0}".format(str(e)))
except FileNotFoundError as e:
	print("Missing file: {0}".format(str(e)))


