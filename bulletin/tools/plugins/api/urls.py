from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

import event.views
import job.views
import new_resource.views
import story.views

urlpatterns = patterns(
    '',

    url(r'^event/$',
        event.views.EventList.as_view(),
        name='event-list'),

    url(r'^event/(?P<pk>[0-9]+)/$',
        event.views.EventDetail.as_view(),
        name='event-detail'),

    url(r'^job/$',
        job.views.JobList.as_view(),
        name='job-list'),

    url(r'^job/(?P<pk>[0-9]+)/$',
        job.views.JobDetail.as_view(),
        name='job-detail'),

    url(r'^new-resource/$',
        new_resource.views.NewResourceList.as_view(),
        name='new-resource-list'),

    url(r'^new-resource/(?P<pk>[0-9]+)/$',
        new_resource.views.NewResourceDetail.as_view(),
        name='new-resource-detail'),

    url(r'^story/$',
        story.views.StoryList.as_view(),
        name='story-list'),

    url(r'^story/(?P<pk>[0-9]+)/$',
        story.views.StoryDetail.as_view(),
        name='story-detail'),
)

urlpatterns = format_suffix_patterns(urlpatterns)
