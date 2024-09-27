from django.urls import include, re_path

from . import views
from .api import urls as api_urls

app_name = 'plugins'

urlpatterns = [
    ########################
    # Generic plugin views #
    ########################
    # List installed plugins:
    re_path(r'^submit/$',
        views.plugin.PluginListView.as_view(),
        name='plugin-list'),

    # Generic submit view.
    re_path(r'^submit-post/$',
        views.plugin.PluginSubmitView.as_view(),
        name='submit'),

    # Generic update view.
    re_path(r'^update-post/(?P<post_type>\w+)/(?P<pk>\d+)$',
        views.plugin.PluginUpdateView.as_view(),
        name='update'),
    ###############################
    # End of generic plugin views #
    ###############################

    re_path(r'^moderation/$',
        views.plugin.ModerationView.as_view(),
        name='moderation'),

    ###############
    # Event views #
    ###############
    # Submit an event:
    re_path(r'^event/submit/$',
        views.event.EventSubmitView.as_view(),
        name='event-submit'),

    # Update an event:
    re_path(r'^event/(?P<pk>\d+)$',
        views.event.EventUpdateView.as_view(),
        name='event-update'),

    # List of events.
    re_path(r'^event/$',
        views.event.EventListView.as_view(),
        name='event-list'),
    ######################
    # End of Event views #
    ######################

    #############
    # Job views #
    #############
    # Submit a job:
    re_path(r'^job/submit/$',
        views.job.JobSubmitView.as_view(),
        name='job-submit'),

    # Update a job:
    re_path(r'^job/(?P<pk>\d+)$',
        views.job.JobUpdateView.as_view(),
        name='job-update'),

    # List of jobs.
    re_path(r'^job/$',
        views.job.JobListView.as_view(),
        name='job-list'),
    ####################
    # End of Job views #
    ####################

    #####################
    # NewResource views #
    #####################
    # Submit a new resource:
    # Same goes for this url as the following. It's turdy.
    re_path(r'^new-resource/submit/$',
        views.new_resource.NewResourceSubmitView.as_view(),
        name='newresource-submit'),

    # Update a new resource:
    # Here's an ugly fact. This url has a magic name. It must be
    # named 'newresource-update' because oh cripes here's a stinking
    # turd - because plugins.view.plugin.PluginUpdateView is going
    # to redirect requests to this URL to `{post-type}-update` where
    # post-type is `newresource`. Not `new-resource`. `newresource-update`
    # it must be.
    re_path(r'^new-resource/(?P<pk>\d+)$',
        views.new_resource.NewResourceUpdateView.as_view(),
        name='newresource-update'),

    # List of new resources.
    re_path(r'^new-resource/$',
        views.new_resource.NewResourceListView.as_view(),
        name='new-resource-list'),
    ############################
    # End of NewResource views #
    ############################

    #####################
    # Opportunity views #
    #####################
    # Submit a opportunity:
    re_path(r'^opportunity/submit/$',
        views.opportunity.OpportunitySubmitView.as_view(),
        name='opportunity-submit'),

    # Update a opportunity:
    re_path(r'^opportunity/(?P<pk>\d+)$',
        views.opportunity.OpportunityUpdateView.as_view(),
        name='opportunity-update'),

    # List of opportunities.
    re_path(r'^opportunity/$',
        views.opportunity.OpportunityListView.as_view(),
        name='opportunity-list'),
    ############################
    # End of Opportunity views #
    ############################

    ###############
    # Story views #
    ###############
    # Submit a story:
    re_path(r'^story/submit/$',
        views.story.StorySubmitView.as_view(),
        name='story-submit'),

    # Update a story:
    re_path(r'^story/(?P<pk>\d+)$',
        views.story.StoryUpdateView.as_view(),
        name='story-update'),

    # List of stories
    re_path(r'^story/$',
        views.story.StoryListView.as_view(),
        name='story-list'),
    ######################
    # End of Story views #
    ######################

    #######
    # API #
    #######
    re_path(r'^api/', include(api_urls)),
]
