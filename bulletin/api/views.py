import json

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.http import HttpResponseServerError
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

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
from django_constant_contact.models import (ConstantContact,
                                            ConstantContactAPIError)
from .serializers import (CategorySerializer,
                          IssueSectionReorderSerializer,
                          IssueTemplateSerializer,
                          LinkSerializer,
                          NewsletterSerializer,
                          SectionSerializer,
                          SectionPostReorderSerializer,
                          SectionTemplateSerializer,
                          PostSerializer,
                          UserSerializer,
                          IssueSerializer,
                          AdSizeSerializer,
                          AdSerializer)
import permissions


@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'newsletters': reverse('bulletin:api:newsletter-list',
                               request=request,
                               format=format),
        })


class RequiredFieldsMissingError(Exception):
    pass


class TemplateProducedNoOutputError(Exception):
    pass


class NewsletterList(generics.ListCreateAPIView):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class NewsletterDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsletterSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Newsletter.objects.get(pk=self.kwargs['pk'])


class NewsletterIssueList(generics.ListCreateAPIView):
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_newsletter(self):
        return Newsletter.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        return Issue.objects.filter(newsletter=self.get_newsletter())

    def perform_create(self, serializer):
        serializer.save(newsletter=self.get_newsletter())


class IssueList(generics.ListCreateAPIView):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Issue.objects.get(pk=self.kwargs['pk'])


class IssueFill(generics.UpdateAPIView):
    """Fill an Issue with Posts.

    Posts that have been approved for inclusion in a newsletter but
    have not yet been included are swept into the Issue.

    Posts are sorted into Sections of the Issue by matching
    Post.primary_category into Section.categories and the ContentType
    of the Post into Section.content_types.

    If there are eligible Posts that can't be mapped into a Section
    (because the Category maps to a non-existant Section, e.g.), a new
    Section will be added to the Issue, named 'Unsorted'.  Posts that
    couldn't be sorted into a Section will be placed here.
    """
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def section_filter(self, section, posts):
        """Filter posts from `posts` that match `section`'s categories and
        content_types.

        Returns two lists, the first the posts that matched, the second
        the remainder.
        """
        matches = []
        misses = []
        for post in posts:
            if (((post.primary_category and
                  post.primary_category in section.categories.all()) or
                 post.primary_category is None) and
                post.content_type in section.content_types.all()):

                matches.append(post)
            else:
                misses.append(post)
        return matches, misses

    def fill_issue(self):
        """Sorts Posts available for inclusion in an Issue into
        this Issue's Sections.

        Posts are placed into Sections by assigning to their
        section attribute.  So there's a bunch of maybe surprising
        side effects for you, lots of Posts updated in fill_issue.
        """
        issue = self.get_object()

        remaining_posts = Post.available_for_newsletter()

        for section in issue.sections.all():

            matched_posts, remaining_posts = self.section_filter(
                section, remaining_posts)

            for post in matched_posts:
                post.section = section
                post.save()

        if remaining_posts:
            try:
                unsorted_section = issue.sections.get(name='Unsorted')
            except Section.DoesNotExist:
                unsorted_section = Section.objects.create(issue=issue,
                                                          name='Unsorted')
            for post in remaining_posts:
                post.section = unsorted_section
                post.save()

    def patch(self, request, **kwargs):
        self.fill_issue()
        return Response(status=status.HTTP_204_NO_CONTENT)


class IssueUpload(generics.RetrieveUpdateDestroyAPIView):
    """Upload, update, and delete an Issue at Constant Contact.

    PUT to upload, PATCH to update, DELETE to delete.
    """
    serializer_class = IssueSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def pre_upload_check(self, issue):
        """Make sure all the data looks cool before uploading to CC.

        Raises an Exception or returns an HttpResponseServerError
        when something looks wonky.

        When everything looks ok, returns None.
        """
        # Make sure data for fields required by Constant Contact is available:
        try:
            self.ensure_required_fields_are_provided()
        except Exception as exc:
            raise ValidationError(exc.message)

        # Make sure render_to_html() works (might not, depending on template):
        try:
            email_content = issue.render_to_html()
        except Exception as exc:
            message = 'render_to_html(): ' + exc.message
            raise ValidationError(message)

        # Make sure render_to_text() works (might not, depending on template):
        try:
            text_content = issue.render_to_text()
        except Exception as exc:
            message = 'render_to_text(): ' + exc.message
            raise ValidationError(message)

        # Make sure both render methods produced something:
        rendering_errors = {}
        if email_content == "":
            rendering_errors['email_content'] = (
                'The template ({template_name}) produced no output.'.format(
                    template_name=issue.html_template_name))
        if text_content == "":
            rendering_errors['text_content'] = (
                'The template ({template_name}) produced no output.'.format(
                    template_name=issue.text_template_name))

        if rendering_errors:
            raise TemplateProducedNoOutputError(json.dumps(rendering_errors))

    def put(self, request, **kwargs):
        """Upload an Issue to Constant Contact.
        """
        issue = self.get_object()

        try:
            self.pre_upload_check(issue)
        except TemplateProducedNoOutputError:
            raise
        except Exception as exc:
            return HttpResponseServerError(content=str(exc))

        email_content = issue.render_to_html()
        text_content = issue.render_to_text()

        constant_contact = ConstantContact()

        try:
            issue.email_marketing_campaign = (
                constant_contact.new_email_marketing_campaign(
                    name=issue.name,
                    from_email=issue.from_email,
                    from_name=issue.from_name,
                    reply_to_email=issue.reply_to_email,
                    subject=issue.subject,
                    email_content=email_content,
                    text_content=text_content,
                    address={'organization_name': issue.organization_name,
                             'address_line_1': issue.address_line_1,
                             'address_line_2': issue.address_line_2,
                             'address_line_3': issue.address_line_3,
                             'city': issue.city,
                             'state': issue.state,
                             'international_state': issue.international_state,
                             'postal_code': issue.postal_code,
                             'country': issue.country}))
        except ConstantContactAPIError as exc:
            content = {
                'ConstantContact.[new|update]_email_markeing_campaign':
                str(exc),
                'errors': exc.errors
            }
            return HttpResponseServerError(content=json.dumps(content))
        except Exception as exc:
            return HttpResponseServerError(str(exc))
        else:
            issue.save()

            serialized_issue = self.serializer_class(issue)

        return Response(status=status.HTTP_202_ACCEPTED,
                        data=serialized_issue.data)

    def patch(self, request, **kwargs):
        """Update an Issue up at Constant Contact.
        """
        issue = self.get_object()

        try:
            self.pre_upload_check(issue)
        except TemplateProducedNoOutputError:
            raise
        except Exception as exc:
            return HttpResponseServerError(content=str(exc))

        email_content = issue.render_to_html()
        text_content = issue.render_to_text()

        constant_contact = ConstantContact()

        try:
            issue.email_marketing_campaign = (
                constant_contact.update_email_marketing_campaign(
                    email_marketing_campaign=issue.email_marketing_campaign,
                    name=issue.name,
                    from_email=issue.from_email,
                    from_name=issue.from_name,
                    reply_to_email=issue.reply_to_email,
                    subject=issue.subject,
                    email_content=email_content,
                    text_content=text_content,
                    address={'organization_name': issue.organization_name,
                             'address_line_1': issue.address_line_1,
                             'address_line_2': issue.address_line_2,
                             'address_line_3': issue.address_line_3,
                             'city': issue.city,
                             'state': issue.state,
                             'international_state': issue.international_state,
                             'postal_code': issue.postal_code,
                             'country': issue.country}))
        except ConstantContactAPIError as exc:
            content = {
                'ConstantContact.[new|update]_email_markeing_campaign':
                str(exc),
                'errors': exc.errors
            }
            return HttpResponseServerError(content=json.dumps(content))
        except Exception as exc:
            return HttpResponseServerError(str(exc))
        else:
            issue.save()

        serialized_issue = self.serializer_class(issue)

        return Response(status=status.HTTP_202_ACCEPTED,
                        data=serialized_issue.data)

    def delete(self, request, **kwargs):
        issue = self.get_object()

        email_marketing_campaign = issue.email_marketing_campaign
        email_marketing_campaign.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)

    def ensure_required_fields_are_provided(self):
        """Make sure each self.get_object().field in `field_names` != blank.

        Raises RequiredFieldsMissingError if any fields are empty.
        """
        field_names = ['name',
                       'from_email',
                       'from_name',
                       'reply_to_email',
                       'subject',
                       'organization_name',
                       'address_line_1',
                       'city',
                       'state',
                       'postal_code',
                       'country',
                       'html_template_name',
                       'text_template_name']
        blank_fields = []

        # check issue fields:
        issue = self.get_object()
        for field_name in field_names:
            if getattr(issue, field_name) in ["", None]:
                blank_fields.append(field_name)

        if blank_fields:
            errors = {}
            for blank_field in blank_fields:
                errors[blank_field] = 'This field is required.'

            raise RequiredFieldsMissingError(json.dumps(errors))


class IssueSectionList(generics.ListCreateAPIView):
    serializer_class = SectionSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_queryset(self):
        return Section.objects.filter(issue=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(issue=Issue.objects.get(pk=self.kwargs['pk']))


class IssueSectionUp(generics.UpdateAPIView):
    """Moves a Section up in an Issue's list of sections.
    """
    serializer_class = IssueSectionReorderSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Section.objects.get(pk=self.kwargs['section_pk'])

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.up()


class IssueSectionDown(generics.UpdateAPIView):
    """Moves a Section down in an Issue's list of sections.
    """
    serializer_class = IssueSectionReorderSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Section.objects.get(pk=self.kwargs['section_pk'])

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.down()


class SectionList(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class SectionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SectionSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Section.objects.get(pk=self.kwargs['pk'])


class SectionPostList(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_queryset(self):
        return Post.objects.filter(section=self.kwargs['pk'])

    def perform_create(self, serializer):
        serializer.save(section=Section.objects.get(pk=self.kwargs['pk']),
                        submitter=self.request.user)


class SectionPostDelete(generics.DestroyAPIView):
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def delete(self, request, **kwargs):
        section = Section.objects.get(pk=self.kwargs['section_pk'])
        post = Post.objects.get(pk=self.kwargs['post_pk'])
        section.posts.remove(post)
        section.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SectionPostUp(generics.UpdateAPIView):
    """Moves a Post up in a Section's list of posts.
    """
    serializer_class = SectionPostReorderSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Post.objects.get(pk=self.kwargs['post_pk'])

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.up()


class SectionPostDown(generics.UpdateAPIView):
    """Moves a Post down in a Section's list of posts.
    """
    serializer_class = SectionPostReorderSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Post.objects.get(pk=self.kwargs['post_pk'])

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.down()


class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(submitter=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Post.objects.get(pk=self.kwargs['pk'])


class LinkDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = LinkSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Link.objects.get(pk=self.kwargs['pk'])


class PostCategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return post.categories.all()


class CategoryList(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class CategoryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Category.objects.get(pk=self.kwargs['pk'])


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return User.objects.get(pk=self.kwargs['pk'])


class IssueTemplateList(generics.ListCreateAPIView):
    queryset = IssueTemplate.objects.all()
    serializer_class = IssueTemplateSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class IssueTemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IssueTemplateSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return IssueTemplate.objects.get(pk=self.kwargs['pk'])


class SectionTemplateList(generics.ListCreateAPIView):
    queryset = SectionTemplate.objects.all()
    serializer_class = SectionTemplateSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class SectionTemplateDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SectionTemplateSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return SectionTemplate.objects.get(pk=self.kwargs['pk'])


class SectionTemplateCategoryList(generics.ListCreateAPIView):
    """List and add to the categories for a section template.
    """
    model = Category
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_section_template(self):
        return SectionTemplate.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        section_template = self.get_section_template()
        return section_template.categories.get_queryset()

    def perform_create(self, serializer):
        import ipdb; ipdb.set_trace()
        section_template = self.get_section_template()
        category = Category.objects.get(pk=self.request.POST['category_id'])
        category.section_templates.add(section_template)
        serialized_category = serializer.save(category=category)
        location = reverse('bulletin:api:category-detail',
                           kwargs={'pk': category.id})
        return Response(status=status.HTTP_201_CREATED,
                        headers={'Location': location},
                        data=serialized_category.data)


class SectionTemplateCategoryDelete(generics.DestroyAPIView):
    """Delete a Category from a SectionTemplate.
    """
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def delete(self, request, **kwargs):
        section_template = SectionTemplate.objects.get(
            pk=self.kwargs['section_template_pk'])
        category = Category.objects.get(pk=self.kwargs['category_pk'])
        category.section_templates.remove(section_template)
        category.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdSizeList(generics.ListCreateAPIView):
    queryset = AdSize.objects.all()
    serializer_class = AdSizeSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class AdSizeDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdSizeSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return AdSize.objects.get(pk=self.kwargs['pk'])


class AdList(generics.ListCreateAPIView):
    queryset = Ad.objects.all()
    serializer_class = AdSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class AdDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)

    def get_object(self):
        return Ad.objects.get(pk=self.kwargs['pk'])
