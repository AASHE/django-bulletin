from django.conf.urls import patterns, include, url

urlpatterns = patterns(
    '',
    url(r'^bulletin/', include('bulletin.urls', namespace='bulletin'))
)
