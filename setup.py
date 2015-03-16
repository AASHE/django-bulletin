#!/usr/bin/env python
from setuptools import setup, find_packages
import os

# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='django-bulletin',
    version='0.1',
    description="A simple newsletter application.",
    author='Bob Erb',
    author_email='bob.erb@aashe.org',
    url='https://github.com/aashe/django-bulletin',
    long_description=read("README.md"),
    packages=[
        'bulletin',
        'bulletin.migrations'
        ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
    ],
    test_suite='tests.main',
    install_requires=[
          "Django==1.6.10",
          "Pillow==2.5.3",
          "South==1.0",
          "django-bootstrap-breadcrumbs==0.7.0",
          "django-bootstrap-pagination==1.5.0",
          "django-bootstrap3==4.11.0",
          "django-braces==1.4.0",
          "django-cors-headers==0.13",
          "django-datetime-widget",
          "django-extensions==1.5.1",
          "django-form-utils",
          "django-jsonfield==0.9.13",
          "django-mathfilters",
          "django-polymorphic",
          "django-positions==0.5.1",
          "django-premailer",
          "django-template-repl",
          "djangorestframework==2.4.2",
          "mailchimp",
          "nap==2.0.0",
          "premailer",
          "psycopg2==2.5.2",
          "python-constant-contact",
          "pytz",
          "sorl-thumbnail",
          "wsgiref==0.1.2",
          "django_constant_contact"],
)
