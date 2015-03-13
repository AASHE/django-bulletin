from django.conf.urls import patterns, include, url

import bulletin

urlpatterns = patterns('',
    url(r'^bulletin/', include('bulletin.urls', namespace='bulletin'))
)
