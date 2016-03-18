#!/usr/bin/env python
from setuptools import setup
import os


# Utility function to read README file
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='django-bulletin',
      version='2.0.4',
      description="A simple newsletter application.",
      author='Bob Erb',
      author_email='bob.erb@aashe.org',
      url='https://github.com/aashe/django-bulletin',
      long_description=read("README.rst"),
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
          "Django>=1.8,<1.9",
          "Pillow==3.1.1",
          "django-bootstrap-breadcrumbs==0.7.0",
          "django-bootstrap-pagination==1.5.0",
          "django-bootstrap3==4.11.0",
          "django-braces==1.4.0",
          "django-constant-contact==1.0.3",
          "django-cors-headers==0.13",
          "django-datetime-widget",
          "django-form-utils",
          "django-haystack==2.4.1",
          "django-jsonfield==0.9.13",
          "django-mathfilters",
          "django-polymorphic==0.7.2",
          "django-positions==0.5.1",
          "djangorestframework==3.3.1",
          "python-constant-contact",
          "pytz",
          "sorl-thumbnail",
          "wsgiref==0.1.2"],
      dependency_links=[
          "git+https://github.com/riltsken/python-constant-contact.git#egg=python_constantcontact-0.1-py2.7.egg"])
