from django.conf import settings
from django.urls import include, re_path
from django.contrib.auth.decorators import login_required
from haystack.query import SearchQuerySet
import haystack.views

from . import views
from bulletin.api import urls as api_urls
from bulletin.decorators import user_passes_test
from bulletin.tools.plugins import urls as plugin_urls
from bulletin.tools.issue_editor import urls as editor_urls


sqs = SearchQuerySet().order_by('-pub_date')

search_view = haystack.views.SearchView(searchqueryset=sqs)

if getattr(settings, "SEARCH_LOGIN_REQUIRED", False):
    try:
        user_test = settings.SEARCH_USER_PASSES_TEST
    except AttributeError:
        user_test = lambda user: True  # noqa because looks fine to me oh

    try:
        user_fails_test_url = settings.SEARCH_USER_FAILS_TEST_URL
    except AttributeError:
        user_fails_test_url = settings.LOGIN_URL

    search_view = user_passes_test(function=search_view,
                                   test_func=user_test,
                                   fail_url=user_fails_test_url)

    search_view = login_required(search_view)

urlpatterns = [
    re_path(r'^$',
        views.FrontPageView.as_view(),
        name='front-page'),

    # url(r'^search/', include('haystack.urls')),

    re_path(r'^search/',
        search_view,
        name='haystack_search'),

    ####################
    # Newsletter views #
    ####################
    # List newsletters:
    re_path(r'^newsletter/list/$',
        views.NewsletterListView.as_view(),
        name='newsletter-list'),

    # Update a newsletter:
    re_path(r'^newsletter/(?P<pk>\w+)/update/$',
        views.NewsletterUpdateView.as_view(),
        name='newsletter-update'),

    # Subscribe to a newsletter:
    re_path(r'^newsletter/(?P<pk>\w+)/subscribe/$',
        views.NewsletterSubscribeView.as_view(),
        name='newsletter-subscribe'),

    re_path(r'newsletter/(?P<pk>\w+)/subscribe/thanks/$',
        views.NewsletterSubscribeThanksView.as_view(),
        name='newsletter-subscribe-thanks'),

    ##########################
    # Newsletter/Issue views #
    ##########################
    # List issues in a newsletter:
    re_path(r'^newsletter/(?P<pk>\w+)/issue/list/$',
        views.NewsletterIssueListView.as_view(),
        name='newsletter-issue-list'),

    # Create an issue in a newsletter:
    re_path(r'^newsletter/(?P<pk>\w+)/issue/add/$',
        views.IssueCreateView.as_view(),
        name='issue-create'),

    ###############
    # Issue views #
    ###############
    # Update an issue:
    re_path(r'^issue/(?P<pk>\w+)/update/$',
        views.IssueUpdateView.as_view(),
        name='issue-update'),

    # Update just the settings for an issue:
    re_path(r'^issue/(?P<pk>\w+)/update-settings/$',
        views.IssueSettingsUpdateView.as_view(),
        name='issue-settings-update'),

    # Delete an issue:
    re_path(r'^issue/(?P<pk>\w+)/delete/$',
        views.IssueDeleteView.as_view(),
        name='issue-delete'),

    # Let user pick template to preview issue with (make sure this
    # one comes before 'issue-preview'):
    re_path(r'^issue/(?P<pk>\w+)/preview/$',
        views.ChooseIssuePreviewTypeView.as_view(),
        name='issue-preview-form'),

    # Preview an issue:
    re_path(r'^issue/(?P<pk>\w+)/preview/(?P<template_name>.*)$',
        views.IssuePreviewView.as_view(),
        name='issue-preview'),

    #######################
    # Issue/Section views #
    #######################
    # List sections in an issue:
    re_path(r'^issue/(?P<pk>\w+)/section/list/$',
        views.IssueSectionListView.as_view(),
        name='issue-section-list'),

    # Create a section in an issue:
    re_path(r'^issue/(?P<pk>\w+)/section/add/$',
        views.SectionCreateView.as_view(),
        name='section-create'),

    #################
    # Section views #
    #################
    # Update a section:
    re_path(r'^section/(?P<pk>\w+)/update/$',
        views.SectionUpdateView.as_view(),
        name='section-update'),

    # Delete a section:
    re_path(r'^section/(?P<pk>\w+)/delete/$',
        views.SectionDeleteView.as_view(),
        name='section-delete'),

    #######################
    # Section/Post views #
    #######################
    # List posts in a section:
    re_path(r'^section/(?P<pk>\w+)/post/list/$',
        views.SectionPostListView.as_view(),
        name='section-post-list'),

    # Add a post to a section:
    re_path(r'^section/(?P<pk>\w+)/post/add/$',
        views.SectionPostAddView.as_view(),
        name='section-post-add'),

    # Remove a post from a section:
    re_path(r'^section/(?P<section_pk>\w+)/remove/(?P<post_pk>\w+)/$',
        views.SectionPostRemoveView.as_view(),
        name='section-post-remove'),

    ###############
    # Post views #
    ###############
    # Submit a post:
    re_path(r'^post/submit/$',
        views.PostSubmitView.as_view(),
        name='post-submit'),

    # Say, "Thanks," for submitting a post:
    re_path(r'^post/thank-you-for-submission/$',
        views.ThankYouForSubmittingPostView.as_view(),
        name='thanks-for-submitting-post'),

    # Update a post:
    re_path(r'^post/(?P<pk>\d+)$',
        views.PostUpdateView.as_view(),
        name='post-update'),

    # List unmoderated Posts:
    re_path(r'^post/unmoderated$',
        views.UnmoderatedPostListView.as_view(),
        name='unmoderated-post-list'),

    ####################
    # Post/Link views  #
    ####################
    # List Links for a Post:
    re_path(r'^post/(?P<pk>\w+)/link/list/$',
        views.PostLinkListView.as_view(),
        name='post-link-list'),

    # Create a Link in a Post:
    re_path(r'^post/(?P<pk>\w+)/link/add/$',
        views.LinkCreateView.as_view(),
        name='link-create'),

    ##############
    # Link views #
    ##############
    # Update a Link:
    re_path(r'link/(?P<pk>\d+)$',
        views.LinkUpdateView.as_view(),
        name='link-update'),

    #############################
    # Post/ScheduledPost views  #
    #############################
    # Create a Link in a Post:
    re_path(r'^post/(?P<pk>\w+)/scheduled-post/add/$',
        views.ScheduledPostCreateView.as_view(),
        name='scheduled-post-create'),

    #######################
    # ScheduledPost views #
    #######################
    # Update a ScheduledPost:
    re_path(r'scheduled-post/(?P<pk>\d+)$',
        views.ScheduledPostUpdateView.as_view(),
        name='scheduled-post-update'),

    ##################################
    # Newsletter/IssueTemplate views #
    ##################################
    # List IssueTemplates for a Newsletter:
    re_path(r'^newsletter/(?P<pk>\w+)/issue-template/list/$',
        views.NewsletterIssueTemplateListView.as_view(),
        name='newsletter-issue-template-list'),

    # Create an IssueTemplate in a Newsletter:
    re_path(r'^newsletter/(?P<pk>\w+)/issue-template/add/$',
        views.IssueTemplateCreateView.as_view(),
        name='issue-template-create'),

    #######################
    # IssueTemplate views #
    #######################
    # Update an IssueTemplate:
    re_path(r'^issue-template/(?P<pk>\w+)/update/$',
        views.IssueTemplateUpdateView.as_view(),
        name='issue-template-update'),

    # Update just the settings of an IssueTemplate:
    re_path(r'^issue-template/(?P<pk>\w+)/update-settings/$',
        views.IssueTemplateSettingsUpdateView.as_view(),
        name='issue-template-settings-update'),

    # Delete an IssueTemplate:
    re_path(r'^issue-template/(?P<pk>\w+)/delete/$',
        views.IssueTemplateDeleteView.as_view(),
        name='issue-template-delete'),

    #######################################
    # IssueTemplate/SectionTemplate views #
    #######################################
    # Create a SectionTemplate in an IssueTemplate:
    re_path(r'^issue-template/(?P<pk>\w+)/section-template/add/$',
        views.SectionTemplateCreateView.as_view(),
        name='section-template-create'),

    #########################
    # SectionTemplate views #
    #########################
    # Update a SectionTemplate:
    re_path(r'^section-template/(?P<pk>\w+)/update/$',
        views.SectionTemplateUpdateView.as_view(),
        name='section-template-update'),

    # Delete a SectionTemplate:
    re_path(r'^section-template/(?P<pk>\w+)/delete/$',
        views.SectionTemplateDeleteView.as_view(),
        name='section-template-delete'),

    #######################################
    # SectionTemplate/IssueTemplate views #
    #######################################
    # List SectionTemplates for an IssueTemplate:
    re_path(r'^issue-template/(?P<pk>\w+)/section-template/list/$',
        views.IssueTemplateSectionTemplateListView.as_view(),
        name='issue-template-section-template-list'),

    ##################################
    # SectionTemplate/Category views #
    ##################################
    # List Categories for a SectionTemplates:
    re_path(r'^section-template/(?P<pk>\w+)/category/list/$',
        views.SectionTemplateCategoryListView.as_view(),
        name='section-template-category-list'),

    # Add a category to a section template:
    re_path(r'^section-template/(?P<pk>\w+)/category/add/$',
        views.SectionTemplateCategoryAddView.as_view(),
        name='section-template-category-add'),

    # Remove a category from a section template:
    re_path(r'^section-template/(?P<section_template_pk>\w+)'
        r'/category/(?P<category_pk>\w+)/remove/$',
        views.SectionTemplateCategoryRemoveView.as_view(),
        name='section-template-category-remove'),

    ############
    # Ad views #
    ############
    # List ads:
    re_path(r'^ad/list/$',
        views.AdListView.as_view(),
        name='ad-list'),

    # Create an ad:
    re_path(r'^ad/add/$',
        views.AdCreateView.as_view(),
        name='ad-create'),

    # Update an ad:
    re_path(r'^ad/(?P<pk>\w+)/update/$',
        views.AdUpdateView.as_view(),
        name='ad-update'),

    # Delete an ad:
    re_path(r'^ad/(?P<pk>\w+)/delete/$',
        views.AdDeleteView.as_view(),
        name='ad-delete'),

    re_path(r'^issue-editor/', include(editor_urls,
                                   namespace='issue-editor')),

    re_path(r'^posts/', include(plugin_urls,
                            namespace='plugins')),

    #######
    # API #
    #######
    re_path(r'^api/', include(api_urls,
                          namespace='api')),
]
