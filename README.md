[![Build Status](https://travis-ci.org/AASHE/django-bulletin.svg?branch=master)](https://travis-ci.org/AASHE/django-bulletin)
[![Coverage Status](https://coveralls.io/repos/AASHE/django-bulletin/badge.svg?branch=master)](https://coveralls.io/r/AASHE/django-bulletin?branch=master)

# django-bulletin

A simple newsletter application.

## Features

  - Primary website listing stories
  - Story submission form for users
  - Newsletter email composition from stories
  - Constant Contact integration
  - Content type plugins

## Installation

1. Add 'django-bulletin' to your requirements.txt file.
2. Add 'bulletin' to your INSTALLED_APPS setting.
3. Run "pip install -r requirements.txt" from your project's directory to install required packages.
4. Run "python manage.py syncdb".
5. Run "python manage.py migrate django_constant_contact". If this is not run before the next command, migration of bulletin, which is before this alphabetically, will fail.
6. Run "python manage.py migrate" to create models for the rest of the apps.

## Settings

The following variables should be set in your settings.py:

    CONSTANT_CONTACT_API_KEY
    CONSTANT_CONTACT_ACCESS_TOKEN
    CONSTANT_CONTACT_FROM_EMAIL
    CONSTANT_CONTACT_REPLY_TO_EMAIL
    CONSTANT_CONTACT_USERNAME
    CONSTANT_CONTACT_PASSWORD

`CONSTANT_CONTACT_API_KEY` is assigned by Constant Contact when
you register your application. (You need to register as a
Constant Contact developer.)

`CONSTANT_CONTACT_ACCESS_TOKEN` is the access token granted to
your application by a Constant Contact user. This is the User
who will own all Constant Contact versions of uploaded Issues.
