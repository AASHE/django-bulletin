from django.conf.urls import patterns, url

from . import views


urlpatterns = patterns(
    '',

    url(r'^newsletter/(?P<pk>\w+)/issue/$',
        views.NewsletterIssueListView.as_view(),
        name='newsletter-issue-list'),
)
