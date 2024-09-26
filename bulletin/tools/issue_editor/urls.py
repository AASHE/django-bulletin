from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^newsletter/(?P<pk>\w+)/issue/$',
        views.NewsletterIssueListView.as_view(),
        name='newsletter-issue-list'),
]
