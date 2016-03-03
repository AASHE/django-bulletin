#!/usr/bin/env python
import logging
import os
import sys

import django

BASE_PATH = os.path.dirname(__file__)

logging.basicConfig()


def main():
    """
    Standalone django model test with a 'memory-only-django-installation'.
    You can play with a django model without a complete django app
    installation.
    http://www.djangosnippets.org/snippets/1044/
    """
    sys.exc_clear()

    os.environ["DJANGO_SETTINGS_MODULE"] = "django.conf.global_settings"
    from django.conf import global_settings

    # Override Settings
    global_settings.ROOT_URLCONF = "bulletin.tests.test_project.urls"

    # Bulletin Settings:
    global_settings.NUM_POSTS_ON_FRONT_PAGE = 10

    global_settings.BULLETIN_CONTENT_TYPE_PLUGINS = (
        'event',
        'job',
        'newresource',
        'opportunity',
        'story',
    )

    global_settings.USE_TZ = True

    BASE_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "bulletin")

    global_settings.STATIC_URL = os.environ.get('STATIC_URL', '/static/')
    global_settings.STATIC_ROOT = os.environ.get(
        'STATIC_ROOT',
        os.path.join(BASE_DIR,
                     global_settings.STATIC_URL.strip('/')))

    global_settings.INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',

        # AASHE Apps
        'bulletin',
        'bulletin.tools.plugins',
        'django_constant_contact',

        'haystack',

        # required by bulletin
        'bootstrap3',
        'bootstrap_pagination',
        'django_bootstrap_breadcrumbs',
    )

    if django.VERSION > (1, 2):
        global_settings.DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'NAME': os.path.join(BASE_PATH, 'connpass.sqlite'),
                'USER': '',
                'PASSWORD': '',
                'HOST': '',
                'PORT': '',
            }
        }
    else:
        global_settings.DATABASE_ENGINE = "sqlite3"
        global_settings.DATABASE_NAME = ":memory:"

    global_settings.MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    global_settings.TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.core.context_processors.debug',
        'django.core.context_processors.i18n',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'django.core.context_processors.tz',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.request'
    )

    # django-constant-contact settings
    global_settings.CONSTANT_CONTACT_API_KEY = os.environ.get(
        'CONSTANT_CONTACT_API_KEY', None)
    global_settings.CONSTANT_CONTACT_ACCESS_TOKEN = os.environ.get(
        'CONSTANT_CONTACT_ACCESS_TOKEN', None)
    global_settings.CONSTANT_CONTACT_FROM_EMAIL = os.environ.get(
        'CONSTANT_CONTACT_FROM_EMAIL', None)
    global_settings.CONSTANT_CONTACT_REPLY_TO_EMAIL = os.environ.get(
        'CONSTANT_CONTACT_REPLY_TO_EMAIL', None)
    global_settings.CONSTANT_CONTACT_USERNAME = os.environ.get(
        'CONSTANT_CONTACT_USERNAME', None)
    global_settings.CONSTANT_CONTACT_PASSWORD = os.environ.get(
        'CONSTANT_CONTACT_PASSWORD', None)
    global_settings.MAILCHIMP_API_KEY = os.environ.get(
        'MAILCHIMP_API_KEY', None)

    global_settings.SECRET_KEY = "blahblah"

    global_settings.SITE_ID = 1

    global_settings.HAYSTACK_CONNECTIONS = {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine'
        },
    }

    global_settings.HAYSTACK_SIGNAL_PROCESSOR = (
        'haystack.signals.RealtimeSignalProcessor')

    django.setup()

    from django.test.utils import get_runner
    test_runner = get_runner(global_settings)

    if django.VERSION > (1, 2):
        test_runner = test_runner()
        failures = test_runner.run_tests(['bulletin'], fail_fast=True)
    else:
        failures = test_runner(['bulletin'], verbosity=1, fail_fast=True)
    sys.exit(failures)

if __name__ == '__main__':
    main()
