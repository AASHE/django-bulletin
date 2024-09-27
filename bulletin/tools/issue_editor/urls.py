from django.urls import re_path

from . import views

app_name = 'issue_editor'

urlpatterns = [
    re_path(r'^newsletter/(?P<pk>\w+)/issue/$',
        views.NewsletterIssueListView.as_view(),
        name='newsletter-issue-list'),
]
