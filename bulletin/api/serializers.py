from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import (Category,
                      Issue,
                      IssueTemplate,
                      Link,
                      Newsletter,
                      Section,
                      SectionTemplate,
                      Post,
                      AdSize,
                      Ad)


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    parent = serializers.RelatedField(read_only=True)
    section_templates = serializers.RelatedField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent', 'fully_qualified_name',
                  'section_templates')


class LinkSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Link
        fields = ('id', 'text', 'url')


class PostSerializer(serializers.HyperlinkedModelSerializer):

    submitter = UserSerializer(required=False, read_only=True)
    links = LinkSerializer(required=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'url', 'approved', 'pub_date',
                  'submitter', 'position', 'links')


class SectionPostReorderSerializer(serializers.HyperlinkedModelSerializer):
    """Used for section-post-up, section-post-down, etc.
    """
    class Meta:
        model = Post
        fields = ('id', 'position')
        read_only_fields = ('position',)


class SectionSerializer(serializers.HyperlinkedModelSerializer):

    posts = PostSerializer(required=False, read_only=True)

    class Meta:
        model = Section
        fields = ('id', 'name', 'posts', 'position')


class IssueSectionReorderSerializer(serializers.HyperlinkedModelSerializer):
    """Used for issue-section-up, issue-section-down, etc.
    """
    class Meta:
        model = Section
        fields = ('id', 'position')
        read_only_fields = ('position',)


class IssueSerializer(serializers.HyperlinkedModelSerializer):

    sections = SectionSerializer(required=False, read_only=True)

    class Meta:
        model = Issue
        fields = ('id', 'pub_date', 'sections', 'name', 'subject',
                  'from_name', 'from_email', 'reply_to_email',
                  'organization_name', 'address_line_1', 'address_line_2',
                  'address_line_3', 'city', 'state', 'international_state',
                  'postal_code', 'country', 'html_template_name',
                  'text_template_name')


class NewsletterSerializer(serializers.HyperlinkedModelSerializer):

    issues = IssueSerializer(required=False, read_only=True)

    class Meta:
        model = Newsletter
        fields = ('id', 'name', 'issues')


class SectionTemplateSerializer(serializers.HyperlinkedModelSerializer):

    categories = CategorySerializer(required=False, read_only=True)

    class Meta:
        model = SectionTemplate
        fields = ('id', 'name', 'position', 'categories')


class IssueTemplateSerializer(serializers.HyperlinkedModelSerializer):

    section_templates = SectionTemplateSerializer(required=False, read_only=True)

    class Meta:
        model = IssueTemplate
        fields = ('id', 'name', 'section_templates', 'subject',
                  'from_name', 'from_email', 'reply_to_email',
                  'organization_name', 'address_line_1', 'address_line_2',
                  'address_line_3', 'city', 'state', 'international_state',
                  'postal_code', 'country', 'html_template_name',
                  'text_template_name')


class AdSizeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AdSize
        fields = ('name', 'width', 'height')


class AdSerializer(serializers.HyperlinkedModelSerializer):

    size = serializers.PrimaryKeyRelatedField(
        queryset=AdSize.objects.all(),
        required=True)

    class Meta:
        model = Ad
        fields = ('name', 'start', 'end', 'size', 'url',
                  'show_on_website', 'include_in_newsletter')
