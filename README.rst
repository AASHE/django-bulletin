========
Bulletin
========

A simple newsletter application.


Quick Start
-----------

1. Add "bulletin" and "bulletin/tools/plugins" to your INSTALLED_APPS settings like this::

    INSTALLED_APPS = (
        ...
        'bulletin',
        'bulletin.tools.plugins',
    )

2. Include the bulletin URLconf in your project urls.py like this::

    url(r'^bulletin/', include('bulletin.urls')),

3. Inside your project root, run 'pip install -r requirements.txt'

3. Inside your project root, run 'python manage.py syncdb'.

4. Inside your project root, run 'python manage.py migrate'.