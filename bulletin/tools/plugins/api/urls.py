from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import event
from . import job
from . import new_resource
from . import story

urlpatterns = [
    re_path(r'^event/$',
        event.views.EventList.as_view(),
        name='event-list'),

    re_path(r'^event/(?P<pk>[0-9]+)/$',
        event.views.EventDetail.as_view(),
        name='event-detail'),

    re_path(r'^job/$',
        job.views.JobList.as_view(),
        name='job-list'),

    re_path(r'^job/(?P<pk>[0-9]+)/$',
        job.views.JobDetail.as_view(),
        name='job-detail'),

    re_path(r'^new-resource/$',
        new_resource.views.NewResourceList.as_view(),
        name='new-resource-list'),

    re_path(r'^new-resource/(?P<pk>[0-9]+)/$',
        new_resource.views.NewResourceDetail.as_view(),
        name='new-resource-detail'),

    re_path(r'^story/$',
        story.views.StoryList.as_view(),
        name='story-list'),

    re_path(r'^story/(?P<pk>[0-9]+)/$',
        story.views.StoryDetail.as_view(),
        name='story-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
