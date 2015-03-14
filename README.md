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
