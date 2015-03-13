from django.conf.urls import include, patterns, url

from . import views
from bulletin.api import urls as api_urls
from bulletin.tools.plugins import urls as plugin_urls
from bulletin.tools.issue_editor import urls as editor_urls


urlpatterns = patterns(
    '',

    url(r'^$',
        views.FrontPageView.as_view(),
        name='front-page'),

    ####################
    # Newsletter views #
    ####################
    # List newsletters:
    url(r'^newsletter/list/$',
        views.NewsletterListView.as_view(),
        name='newsletter-list'),

    # Update a newsletter:
    url(r'^newsletter/(?P<pk>\w+)/update/$',
        views.NewsletterUpdateView.as_view(),
        name='newsletter-update'),

    # Subscribe to a newsletter:
    url(r'^newsletter/(?P<pk>\w+)/subscribe/$',
        views.NewsletterSubscribeView.as_view(),
        name='newsletter-subscribe'),

    url(r'newsletter/(?P<pk>\w+)/subscribe/thanks/$',
        views.NewsletterSubscribeThanksView.as_view(),
        name='newsletter-subscribe-thanks'),

    ##########################
    # Newsletter/Issue views #
    ##########################
    # List issues in a newsletter:
    url(r'^newsletter/(?P<pk>\w+)/issue/list/$',
        views.NewsletterIssueListView.as_view(),
        name='newsletter-issue-list'),

    # Create an issue in a newsletter:
    url(r'^newsletter/(?P<pk>\w+)/issue/add/$',
        views.IssueCreateView.as_view(),
        name='issue-create'),

    ###############
    # Issue views #
    ###############
    # Update an issue:
    url(r'^issue/(?P<pk>\w+)/update/$',
        views.IssueUpdateView.as_view(),
        name='issue-update'),

    # Update just the settings for an issue:
    url(r'^issue/(?P<pk>\w+)/update-settings/$',
        views.IssueSettingsUpdateView.as_view(),
        name='issue-settings-update'),

    # Delete an issue:
    url(r'^issue/(?P<pk>\w+)/delete/$',
        views.IssueDeleteView.as_view(),
        name='issue-delete'),

    # Let user pick template to preview issue with (make sure this
    # one comes before 'issue-preview'):
    url(r'^issue/(?P<pk>\w+)/preview/$',
        views.ChooseIssuePreviewTypeView.as_view(),
        name='issue-preview-form'),

    # Preview an issue:
    url(r'^issue/(?P<pk>\w+)/preview/(?P<template_name>.*)$',
        views.IssuePreviewView.as_view(),
        name='issue-preview'),

    #######################
    # Issue/Section views #
    #######################
    # List sections in an issue:
    url(r'^issue/(?P<pk>\w+)/section/list/$',
        views.IssueSectionListView.as_view(),
        name='issue-section-list'),

    # Create a section in an issue:
    url(r'^issue/(?P<pk>\w+)/section/add/$',
        views.SectionCreateView.as_view(),
        name='section-create'),

    #################
    # Section views #
    #################
    # Update a section:
    url(r'^section/(?P<pk>\w+)/update/$',
        views.SectionUpdateView.as_view(),
        name='section-update'),

    # Delete a section:
    url(r'^section/(?P<pk>\w+)/delete/$',
        views.SectionDeleteView.as_view(),
        name='section-delete'),

    #######################
    # Section/Post views #
    #######################
    # List posts in a section:
    url(r'^section/(?P<pk>\w+)/post/list/$',
        views.SectionPostListView.as_view(),
        name='section-post-list'),

    # Add a post to a section:
    url(r'^section/(?P<pk>\w+)/post/add/$',
        views.SectionPostAddView.as_view(),
        name='section-post-add'),

    # Remove a post from a section:
    url(r'^section/(?P<section_pk>\w+)/remove/(?P<post_pk>\w+)/$',
        views.SectionPostRemoveView.as_view(),
        name='section-post-remove'),

    ###############
    # Post views #
    ###############
    # Submit a post:
    url(r'^post/submit/$',
        views.PostSubmitView.as_view(),
        name='post-submit'),

    # Say, "Thanks," for submitting a post:
    url(r'^post/thank-you-for-submission/$',
        views.ThankYouForSubmittingPostView.as_view(),
        name='thanks-for-submitting-post'),

    # Update a post:
    url(r'^post/(?P<pk>\d+)$',
        views.PostUpdateView.as_view(),
        name='post-update'),

    # List unmoderated Posts:
    url(r'^post/unmoderated$',
        views.UnmoderatedPostListView.as_view(),
        name='unmoderated-post-list'),

    ####################
    # Post/Link views  #
    ####################
    # List Links for a Post:
    url(r'^post/(?P<pk>\w+)/link/list/$',
        views.PostLinkListView.as_view(),
        name='post-link-list'),

    # Create a Link in a Post:
    url(r'^post/(?P<pk>\w+)/link/add/$',
        views.LinkCreateView.as_view(),
        name='link-create'),

    ##############
    # Link views #
    ##############
    # Update a Link:
    url(r'link/(?P<pk>\d+)$',
        views.LinkUpdateView.as_view(),
        name='link-update'),

    ##################################
    # Newsletter/IssueTemplate views #
    ##################################
    # List IssueTemplates for a Newsletter:
    url(r'^newsletter/(?P<pk>\w+)/issue-template/list/$',
        views.NewsletterIssueTemplateListView.as_view(),
        name='newsletter-issue-template-list'),

    # Create an IssueTemplate in a Newsletter:
    url(r'^newsletter/(?P<pk>\w+)/issue-template/add/$',
        views.IssueTemplateCreateView.as_view(),
        name='issue-template-create'),

    #######################
    # IssueTemplate views #
    #######################
    # Update an IssueTemplate:
    url(r'^issue-template/(?P<pk>\w+)/update/$',
        views.IssueTemplateUpdateView.as_view(),
        name='issue-template-update'),

    # Update just the settings of an IssueTemplate:
    url(r'^issue-template/(?P<pk>\w+)/update-settings/$',
        views.IssueTemplateSettingsUpdateView.as_view(),
        name='issue-template-settings-update'),

    # Delete an IssueTemplate:
    url(r'^issue-template/(?P<pk>\w+)/delete/$',
        views.IssueTemplateDeleteView.as_view(),
        name='issue-template-delete'),

    #######################################
    # IssueTemplate/SectionTemplate views #
    #######################################
    # Create a SectionTemplate in an IssueTemplate:
    url(r'^issue-template/(?P<pk>\w+)/section-template/add/$',
        views.SectionTemplateCreateView.as_view(),
        name='section-template-create'),

    #########################
    # SectionTemplate views #
    #########################
    # Update a SectionTemplate:
    url(r'^section-template/(?P<pk>\w+)/update/$',
        views.SectionTemplateUpdateView.as_view(),
        name='section-template-update'),

    # Delete a SectionTemplate:
    url(r'^section-template/(?P<pk>\w+)/delete/$',
        views.SectionTemplateDeleteView.as_view(),
        name='section-template-delete'),

    #######################################
    # SectionTemplate/IssueTemplate views #
    #######################################
    # List SectionTemplates for an IssueTemplate:
    url(r'^issue-template/(?P<pk>\w+)/section-template/list/$',
        views.IssueTemplateSectionTemplateListView.as_view(),
        name='issue-template-section-template-list'),

    ##################################
    # SectionTemplate/Category views #
    ##################################
    # List Categories for a SectionTemplates:
    url(r'^section-template/(?P<pk>\w+)/category/list/$',
        views.SectionTemplateCategoryListView.as_view(),
        name='section-template-category-list'),

    # Add a category to a section template:
    url(r'^section-template/(?P<pk>\w+)/category/add/$',
        views.SectionTemplateCategoryAddView.as_view(),
        name='section-template-category-add'),

    # Remove a category from a section template:
    url(r'^section-template/(?P<section_template_pk>\w+)'
        r'/category/(?P<category_pk>\w+)/remove/$',
        views.SectionTemplateCategoryRemoveView.as_view(),
        name='section-template-category-remove'),

    ############
    # Ad views #
    ############
    # List ads:
    url(r'^ad/list/$',
        views.AdListView.as_view(),
        name='ad-list'),

    # Create an ad:
    url(r'^ad/add/$',
        views.AdCreateView.as_view(),
        name='ad-create'),

    # Update an ad:
    url(r'^ad/(?P<pk>\w+)/update/$',
        views.AdUpdateView.as_view(),
        name='ad-update'),

    # Delete an ad:
    url(r'^ad/(?P<pk>\w+)/delete/$',
        views.AdDeleteView.as_view(),
        name='ad-delete'),

    url(r'^issue-editor/', include(editor_urls,
                     namespace='issue-editor',
                     app_name='Issue Editor')),

    url(r'^plugins/', include(plugin_urls,
                   namespace='plugins',
                   app_name='Plugins')),

    #######
    # API #
    #######
    url(r'^api/', include(api_urls,
                          namespace='api',
                          app_name='Newsletter API')),
)
