from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns

import views


urlpatterns = patterns(
    '',

    url(r'^$', views.api_root, name='newsletter-api-root'),

    url(r'^newsletter/$',
        views.NewsletterList.as_view(),
        name='newsletter-list'),

    url(r'^newsletter/(?P<pk>[0-9]+)/$',
        views.NewsletterDetail.as_view(),
        name='newsletter-detail'),

    url(r'^newsletter/(?P<pk>[0-9]+)/issue/$',
        views.NewsletterIssueList.as_view(),
        name='newsletter-issue-list'),

    url(r'^issue/$',
        views.IssueList.as_view(),
        name='issue-list'),

    url(r'^issue/(?P<pk>[0-9]+)/$',
        views.IssueDetail.as_view(),
        name='issue-detail'),

    url(r'^issue/(?P<pk>[0-9]+)/fill/$',
        views.IssueFill.as_view(),
        name='issue-fill'),

    url(r'^issue/(?P<pk>[0-9]+)/upload/$',
        views.IssueUpload.as_view(),
        name='issue-upload'),

    url(r'^issue/(?P<pk>[0-9]+)/section/$',
        views.IssueSectionList.as_view(),
        name='issue-section-list'),

    url(r'^issue/(?P<issue_pk>[0-9]+)/section/(?P<section_pk>[0-9]+)/up/$',
        views.IssueSectionUp.as_view(),
        name='issue-section-up'),

    url(r'^issue/(?P<issue_pk>[0-9]+)/section/(?P<section_pk>[0-9]+)/down/$',
        views.IssueSectionDown.as_view(),
        name='issue-section-down'),

    url(r'^section/$',
        views.SectionList.as_view(),
        name='section-list'),

    url(r'^section/(?P<pk>[0-9]+)/$',
        views.SectionDetail.as_view(),
        name='section-detail'),

    url(r'^section/(?P<pk>[0-9]+)/post/$',
        views.SectionPostList.as_view(),
        name='section-post-list'),

    url(r'^section/(?P<section_pk>[0-9]+)/post/(?P<post_pk>[0-9]+)/$',
        views.SectionPostDelete.as_view(),
        name='section-post-delete'),

    url(r'^post/$',
        views.PostList.as_view(),
        name='post-list'),

    url(r'^post/(?P<pk>[0-9]+)/$',
        views.PostDetail.as_view(),
        name='post-detail'),

    url(r'link/(?P<pk>[0-9]+)/$',
        views.LinkDetail.as_view(),
        name='link-detail'),

    url(r'^post/(?P<pk>[0-9]+)/category/$',
        views.PostCategoryList.as_view(),
        name='post-category-list'),

    url(r'^section/(?P<section_pk>[0-9]+)/post/(?P<post_pk>[0-9]+)/up/$',
        views.SectionPostUp.as_view(),
        name='section-post-up'),

    url(r'^section/(?P<section_pk>[0-9]+)/post/(?P<post_pk>[0-9]+)/down/$',
        views.SectionPostDown.as_view(),
        name='section-post-down'),

    url(r'^category/$',
        views.CategoryList.as_view(),
        name='category-list'),

    url(r'^category/(?P<pk>[0-9]+)/$',
        views.CategoryDetail.as_view(),
        name='category-detail'),

    url(r'^issue-template/$',
        views.IssueTemplateList.as_view(),
        name='issue-template-list'),

    url(r'^issue-template/(?P<pk>[0-9]+)/$',
        views.IssueTemplateDetail.as_view(),
        name='issue-template-detail'),

    url(r'^section-template/$',
        views.SectionTemplateList.as_view(),
        name='section-template-list'),

    url(r'^section-template/(?P<pk>[0-9]+)/$',
        views.SectionTemplateDetail.as_view(),
        name='section-template-detail'),

    # List of a SectionTemplate's Categories:
    url(r'^section-template/(?P<pk>[0-9]+)/category/$',
        views.SectionTemplateCategoryList.as_view(),
        name='section-template-category-list'),

    # Delete the link between a SectionTemplate and a Category:
    url(r'^section-template/(?P<section_template_pk>[0-9]+)/'
        r'category/(?P<category_pk>[0-9]+)/$',
        views.SectionTemplateCategoryDelete.as_view(),
        name='section-template-category-delete'),

    url(r'^ad-size/$',
        views.AdSizeList.as_view(),
        name='ad-size-list'),

    url(r'^ad-size/(?P<pk>[0-9]+)/$',
        views.AdSizeDetail.as_view(),
        name='ad-size-detail'),

    url(r'^ad/$',
        views.AdList.as_view(),
        name='ad-list'),

    url(r'^ad/(?P<pk>[0-9]+)/$',
        views.AdDetail.as_view(),
        name='ad-detail'),
)


urlpatterns = format_suffix_patterns(urlpatterns)
