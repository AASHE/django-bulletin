========
Bulletin
========

A simple newsletter application.


Quick Start
-----------

1. Add "bulletin" to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = (
        ...
        'bulletin',
    )

2. Include the pulls URLconf in your project urls.py like this::

    url(r'^bulletin/', include('bulletin.urls')),

3. Run 'python manage.py syncdb' to create the bulletin models.