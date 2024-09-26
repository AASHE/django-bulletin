from django.urls import re_path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    re_path(r'^$', views.api_root, name='newsletter-api-root'),

    re_path(r'^newsletter/$',
        views.NewsletterList.as_view(),
        name='newsletter-list'),

    re_path(r'^newsletter/(?P<pk>[0-9]+)/$',
        views.NewsletterDetail.as_view(),
        name='newsletter-detail'),

    re_path(r'^newsletter/(?P<pk>[0-9]+)/issue/$',
        views.NewsletterIssueList.as_view(),
        name='newsletter-issue-list'),

    re_path(r'^issue/$',
        views.IssueList.as_view(),
        name='issue-list'),

    re_path(r'^issue/(?P<pk>[0-9]+)/$',
        views.IssueDetail.as_view(),
        name='issue-detail'),

    re_path(r'^issue/(?P<pk>[0-9]+)/fill/$',
        views.IssueFill.as_view(),
        name='issue-fill'),

    re_path(r'^issue/(?P<pk>[0-9]+)/upload/$',
        views.IssueUpload.as_view(),
        name='issue-upload'),

    re_path(r'^issue/(?P<pk>[0-9]+)/section/$',
        views.IssueSectionList.as_view(),
        name='issue-section-list'),

    re_path(r'^issue/(?P<issue_pk>[0-9]+)/section/(?P<section_pk>[0-9]+)/up/$',
        views.IssueSectionUp.as_view(),
        name='issue-section-up'),

    re_path(r'^issue/(?P<issue_pk>[0-9]+)/section/(?P<section_pk>[0-9]+)/down/$',
        views.IssueSectionDown.as_view(),
        name='issue-section-down'),

    re_path(r'^section/$',
        views.SectionList.as_view(),
        name='section-list'),

    re_path(r'^section/(?P<pk>[0-9]+)/$',
        views.SectionDetail.as_view(),
        name='section-detail'),

    re_path(r'^section/(?P<pk>[0-9]+)/post/$',
        views.SectionPostList.as_view(),
        name='section-post-list'),

    re_path(r'^section/(?P<section_pk>[0-9]+)/post/(?P<post_pk>[0-9]+)/$',
        views.SectionPostDelete.as_view(),
        name='section-post-delete'),

    re_path(r'^post/$',
        views.PostList.as_view(),
        name='post-list'),

    re_path(r'^post/(?P<pk>[0-9]+)/$',
        views.PostDetail.as_view(),
        name='post-detail'),

    re_path(r'^post/(?P<pk>[0-9]+)/schedule/$',
        views.SchedulePost.as_view(),
        name='schedule-post'),

    re_path(r'^scheduled-post/(?P<pk>[0-9]+)/$',
        views.ScheduledPostDetail.as_view(),
        name='scheduled-post-detail'),

    re_path(r'link/(?P<pk>[0-9]+)/$',
        views.LinkDetail.as_view(),
        name='link-detail'),

    re_path(r'^post/(?P<pk>[0-9]+)/category/$',
        views.PostCategoryList.as_view(),
        name='post-category-list'),

    re_path(r'^section/(?P<section_pk>[0-9]+)/post/(?P<post_pk>[0-9]+)/up/$',
        views.SectionPostUp.as_view(),
        name='section-post-up'),

    re_path(r'^section/(?P<section_pk>[0-9]+)/post/(?P<post_pk>[0-9]+)/down/$',
        views.SectionPostDown.as_view(),
        name='section-post-down'),

    re_path(r'^category/$',
        views.CategoryList.as_view(),
        name='category-list'),

    re_path(r'^category/(?P<pk>[0-9]+)/$',
        views.CategoryDetail.as_view(),
        name='category-detail'),

    re_path(r'^issue-template/$',
        views.IssueTemplateList.as_view(),
        name='issue-template-list'),

    re_path(r'^issue-template/(?P<pk>[0-9]+)/$',
        views.IssueTemplateDetail.as_view(),
        name='issue-template-detail'),

    re_path(r'^section-template/$',
        views.SectionTemplateList.as_view(),
        name='section-template-list'),

    re_path(r'^section-template/(?P<pk>[0-9]+)/$',
        views.SectionTemplateDetail.as_view(),
        name='section-template-detail'),

    # List of a SectionTemplate's Categories:
    re_path(r'^section-template/(?P<pk>[0-9]+)/category/$',
        views.SectionTemplateCategoryList.as_view(),
        name='section-template-category-list'),

    # Delete the link between a SectionTemplate and a Category:
    re_path(r'^section-template/(?P<section_template_pk>[0-9]+)/'
        r'category/(?P<category_pk>[0-9]+)/$',
        views.SectionTemplateCategoryDelete.as_view(),
        name='section-template-category-delete'),

    re_path(r'^ad-size/$',
        views.AdSizeList.as_view(),
        name='ad-size-list'),

    re_path(r'^ad-size/(?P<pk>[0-9]+)/$',
        views.AdSizeDetail.as_view(),
        name='ad-size-detail'),

    re_path(r'^ad/$',
        views.AdList.as_view(),
        name='ad-list'),

    re_path(r'^ad/(?P<pk>[0-9]+)/$',
        views.AdDetail.as_view(),
        name='ad-detail'),
]


urlpatterns = format_suffix_patterns(urlpatterns)
