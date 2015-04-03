from django.conf.urls import include, patterns, url

import views
from api import urls as api_urls


urlpatterns = patterns(
    '',

    ########################
    # Generic plugin views #
    ########################
    # List installed plugins:
    url(r'^submit/$',
        views.plugin.PluginListView.as_view(),
        name='plugin-list'),

    # Generic submit view.
    url(r'^submit-post/$',
        views.plugin.PluginSubmitView.as_view(),
        name='submit'),

    # Generic update view.
    url(r'^update-post/(?P<post_type>\w+)/(?P<pk>\d+)$',
        views.plugin.PluginUpdateView.as_view(),
        name='update'),
    ###############################
    # End of generic plugin views #
    ###############################

    url(r'^moderation/$',
        views.plugin.ModerationView.as_view(),
        name='moderation'),

    ###############
    # Event views #
    ###############
    # Submit an event:
    url(r'^event/submit/$',
        views.event.EventSubmitView.as_view(),
        name='event-submit'),

    # Update an event:
    url(r'^event/(?P<pk>\d+)$',
        views.event.EventUpdateView.as_view(),
        name='event-update'),

    # List of events.
    url(r'^event/$',
        views.event.EventListView.as_view(),
        name='event-list'),
    ######################
    # End of Event views #
    ######################

    #############
    # Job views #
    #############
    # Submit a job:
    url(r'^job/submit/$',
        views.job.JobSubmitView.as_view(),
        name='job-submit'),

    # Update a job:
    url(r'^job/(?P<pk>\d+)$',
        views.job.JobUpdateView.as_view(),
        name='job-update'),

    # List of jobs.
    url(r'^job/$',
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
    url(r'^new-resource/submit/$',
        views.new_resource.NewResourceSubmitView.as_view(),
        name='newresource-submit'),

    # Update a new resource:
    # Here's an ugly fact. This url has a magic name. It must be
    # named 'newresource-update' because oh cripes here's a stinking
    # turd - because plugins.view.plugin.PluginUpdateView is going
    # to redirect requests to this URL to `{post-type}-update` where
    # post-type is `newresource`. Not `new-resource`. `newresource-update`
    # it must be.
    url(r'^new-resource/(?P<pk>\d+)$',
        views.new_resource.NewResourceUpdateView.as_view(),
        name='newresource-update'),

    # List of new resources.
    url(r'^new-resource/$',
        views.new_resource.NewResourceListView.as_view(),
        name='new-resource-list'),
    ############################
    # End of NewResource views #
    ############################

    #####################
    # Opportunity views #
    #####################
    # Submit a opportunity:
    url(r'^opportunity/submit/$',
        views.opportunity.OpportunitySubmitView.as_view(),
        name='opportunity-submit'),

    # Update a opportunity:
    url(r'^opportunity/(?P<pk>\d+)$',
        views.opportunity.OpportunityUpdateView.as_view(),
        name='opportunity-update'),

    # List of opportunities.
    url(r'^opportunity/$',
        views.opportunity.OpportunityListView.as_view(),
        name='opportunity-list'),
    ############################
    # End of Opportunity views #
    ############################

    ###############
    # Story views #
    ###############
    # Submit a story:
    url(r'^story/submit/$',
        views.story.StorySubmitView.as_view(),
        name='story-submit'),

    # Update a story:
    url(r'^story/(?P<pk>\d+)$',
        views.story.StoryUpdateView.as_view(),
        name='story-update'),

    # List of stories
    url(r'^story/$',
        views.story.StoryListView.as_view(),
        name='story-list'),
    ######################
    # End of Story views #
    ######################

    #######
    # API #
    #######
    url(r'^api/', include(api_urls,
                          namespace='api',
                          app_name='Newsletter Plugins API')),
)
