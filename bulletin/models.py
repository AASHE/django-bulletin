import datetime

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.template.response import SimpleTemplateResponse
import polymorphic
from positions.fields import PositionField
from python_constantcontact import cc
import pytz

from django_constant_contact.models import EmailMarketingCampaign


class BadEmailAddress(Exception):
    pass


class Newsletter(models.Model):

    name = models.CharField(max_length=255,
                            unique=True)
    # mailing_list is the name of the Constant Contact email
    # list that represents subscribers to this newsletter.
    mailing_list = models.CharField(max_length=255,
                                    blank=True,
                                    null=True)

    def __unicode__(self):
        return self.name

    def subscribe(self, email):
        api = cc.Api(api_key=settings.CONSTANT_CONTACT_API_KEY,
                     username=settings.CONSTANT_CONTACT_USERNAME,
                     password=settings.CONSTANT_CONTACT_PASSWORD)

        # Get the number portion of AASHE Events list id:
        mailing_lists = api.get_collection()
        mailing_list = [mailing_list for
                        mailing_list in mailing_lists.entries
                        if mailing_list.title == self.mailing_list][0]
        mailing_list_id_number = mailing_list.id.split('/')[-1]

        try:
            api.get_contact_by_email(email)
        except cc.HTTPNotFound:
            # Create a new contact, and subscribe it:
            try:
                api.create_contact(email, [mailing_list_id_number])
            except cc.HTTPBadRequest as exc:
                if exc.status.status == 400:
                    raise BadEmailAddress(email)
                else:
                    raise
            return
        else:
            # Subscribe existing contact to AASHE Events list:
            api.add_contact_to_lists_by_email(email,
                                              [mailing_list_id_number])


class Issue(models.Model):

    newsletter = models.ForeignKey(Newsletter,
                                   related_name='issues')
    pub_date = models.DateField(null=True,
                                blank=True)
    html_template_name = models.CharField(max_length=1024,
                                          null=True,
                                          blank=True)
    text_template_name = models.CharField(max_length=1024,
                                          null=True,
                                          blank=True)
    email_marketing_campaign = models.OneToOneField(EmailMarketingCampaign,
                                                    null=True,
                                                    blank=True,
                                                    on_delete=models.SET_NULL)
    introduction = models.TextField(null=True, blank=True)

    # The following are fields required by Constant Contact:
    name = models.CharField(max_length=128)
    subject = models.CharField(max_length=128,
                               null=True)
    from_name = models.CharField(max_length=128,
                                 null=True)
    from_email = models.EmailField(null=True)
    reply_to_email = models.EmailField(null=True)
    organization_name = models.CharField(max_length=128,
                                         null=True)
    address_line_1 = models.CharField(max_length=128,
                                      null=True)
    address_line_2 = models.CharField(max_length=128,
                                      blank=True,
                                      null=True)
    address_line_3 = models.CharField(max_length=128,
                                      blank=True,
                                      null=True)
    city = models.CharField(max_length=128,
                            null=True)
    state = models.CharField(max_length=128,
                             null=True)
    international_state = models.CharField(max_length=128,
                                           blank=True,
                                           null=True)
    postal_code = models.CharField(max_length=128,
                                   null=True)
    country = models.CharField(max_length=128,
                               null=True)

    class Meta:
        ordering = ('-pub_date',)

    def __unicode__(self):
        return '{name}'.format(name=self.name)

    def init_from_issue_template(self, issue_template):
        """Initialize this Issue from an IssueTemplate.
        """
        for field_name in ('subject', 'from_name', 'from_email',
                           'reply_to_email', 'organization_name',
                           'address_line_1', 'address_line_2',
                           'address_line_3', 'city', 'state',
                           'international_state', 'postal_code',
                           'country', 'html_template_name',
                           'text_template_name'):
            setattr(self, field_name, getattr(issue_template, field_name))
        self.save()

        for section_template in issue_template.section_templates.all():
            section = Section.objects.create(name=section_template.name,
                                             issue=self)
            for category in section_template.categories.all():
                category.sections.add(section)
                category.save()
            for content_type in section_template.content_types.all():
                section.content_types.add(content_type)
                section.save()

    def get_context_data(self):
        """Provides a context for rendering this issue.
        """
        return {'issue': self,
                'ads': Ad.ads_for(date=self.pub_date,
                                  include_in_newsletter=True),
                'domain': Site.objects.get_current().domain}

    def _render(self, template_name):
        response = SimpleTemplateResponse(
            template=template_name,
            context=self.get_context_data())
        response.render()
        return response.content

    def render_to_html(self, html_template_name=None):
        """Returns an HTML representation of this Issue.

        Defaults to using the Django template specified by
        self.html_template_name, which can be overridden by
        passing in `html_template_name`.
        """
        html_template_name = html_template_name or self.html_template_name
        return self._render(template_name=html_template_name)

    def render_to_text(self, text_template_name=None):
        """Returns a text representation of this Issue.

        Defaults to using the Django template specified by
        self.text_template_name, which can be overridden by
        passing in `text_template_name`.
        """
        text_template_name = text_template_name or self.text_template_name
        return self._render(template_name=text_template_name)


class Category(models.Model):

    name = models.CharField(max_length=255)
    parent = models.ForeignKey("self",
                               null=True,
                               blank=True)
    fully_qualified_name = models.CharField(max_length=1024,
                                            null=True,
                                            blank=True)
    image = models.ImageField(max_length=512,
                              upload_to='django-bulletin/%Y/%m/%d/category',
                              null=True,
                              blank=True)
    url = models.URLField(max_length=640,
                          null=True,
                          blank=True)

    class Meta:
        ordering = ['fully_qualified_name']
        verbose_name_plural = 'categories'
        unique_together = ('parent', 'name')

    def _fully_qualified_name(self, delimiter='/'):
        if self.parent:
            return delimiter.join(
                [self.parent._fully_qualified_name(delimiter),
                 self.name])
        else:
            return self.name

    def save(self, *args, **kwargs):
        self.fully_qualified_name = self._fully_qualified_name()
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name


class Section(models.Model):

    name = models.CharField(max_length=255)
    issue = models.ForeignKey(Issue,
                              related_name='sections')
    position = models.IntegerField(null=True,
                                   blank=True)
    categories = models.ManyToManyField(Category,
                                        related_name='sections',
                                        null=True,
                                        blank=True)
    content_types = models.ManyToManyField(ContentType,
                                           null=True,
                                           blank=True)

    class Meta:
        ordering = ('issue', 'position')
        unique_together = ('issue', 'name')

    def __unicode__(self):
        return unicode(self.issue) + ': ' + self.name

    def up(self):
        previous_section = self.issue.sections.filter(
            position__lt=self.position).last()
        if previous_section:
            self.position, previous_section.position = (
                previous_section.position, self.position)
            with transaction.atomic():
                self.save()
                previous_section.save()
        # else, already at start of list

    def down(self):
        next_section = self.issue.sections.filter(
            position__gt=self.position).first()
        if next_section:
            self.position, next_section.position = (
                next_section.position, self.position)
            with transaction.atomic():
                self.save()
                next_section.save()
        # else, already at end of list

    def save(self, *args, **kwargs):
        if self.issue and self.position is None:
            self.position = self.issue.sections.count() + 1
        elif self.issue is None:
            self.position = None
        return super(Section, self).save(*args, **kwargs)


class Post(polymorphic.PolymorphicModel):

    date_submitted = models.DateTimeField(auto_now_add=True)
    # Required fields:
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=255)
    submitter = models.ForeignKey(User)
    # Optional fields:
    approved = models.NullBooleanField(null=True)
    include_in_newsletter = models.BooleanField(default=True,
                                                blank=True)
    feature = models.BooleanField(default=False,
                                  blank=True)
    pub_date = models.DateTimeField(blank=True,
                                    null=True)
    category = models.ForeignKey(Category,
                                 related_name='posts',
                                 null=True,
                                 blank=True,
                                 on_delete=models.SET_NULL)
    section = models.ForeignKey(Section,
                                related_name='posts',
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL)
    position = models.IntegerField(null=True,
                                   blank=True)
    image = models.ImageField(max_length=512,
                              upload_to='django-bulletin/%Y/%m/%d/post',
                              null=True,
                              blank=True)

    class Meta:
        ordering = ('section', 'position')

    @classmethod
    def available_for_newsletter(cls):
        """Returns all Posts available to be included in a Newsletter.

        A Post must meet two criteria to be available for a Newsletter;

            1. it must be approved for inclusion in a Newsletter, and;

            2. it must not have been previously included in a Newsletter.
        """
        available_posts = Post.objects.filter(approved=True,
                                              include_in_newsletter=True,
                                              section=None)
        return available_posts

    def __unicode__(self):
        return self.title

    def up(self):
        previous_post = self.section.posts.filter(
            position__lt=self.position).last()
        if previous_post:
            self.position, previous_post.position = (
                previous_post.position, self.position)
            with transaction.atomic():
                self.save()
                previous_post.save()
        # else, already at start of list

    def down(self):
        next_post = self.section.posts.filter(
            position__gt=self.position).first()
        if next_post:
            self.position, next_post.position = (
                next_post.position, self.position)
            with transaction.atomic():
                self.save()
                next_post.save()
        # else, already at end of list

    @property
    def content_type(self):
        content_type = ContentType.objects.get_for_id(
            self.polymorphic_ctype_id)
        return content_type

    def save(self, *args, **kwargs):
        if self.approved and not self.pub_date:
            self.pub_date = datetime.datetime.now(pytz.utc)
        if self.section and self.position is None:
            self.position = self.section.posts.count() + 1
        elif self.section is None:
            self.position = None
        return super(Post, self).save(*args, **kwargs)


class Link(models.Model):

    url = models.URLField(max_length=1024)
    text = models.CharField(max_length=255)
    post = models.ForeignKey(Post,
                             blank=True,
                             related_name='links')

    def __unicode__(self):
        return self.text


class IssueTemplate(models.Model):

    newsletter = models.ForeignKey(Newsletter, blank=True,
                                   related_name='issue_templates')
    # NB: `name` is the name of this IssueTemplate.
    name = models.CharField(max_length=128,
                            unique=True)

    # The following fields are copied over into an Issue when
    # it calls init_from_template():
    subject = models.CharField(max_length=128, null=True, blank=True)
    from_name = models.CharField(max_length=128, null=True, blank=True)
    from_email = models.EmailField(null=True, blank=True)
    reply_to_email = models.EmailField(null=True, blank=True)
    organization_name = models.CharField(max_length=128, null=True,
                                         blank=True)
    address_line_1 = models.CharField(max_length=128, null=True, blank=True)
    address_line_2 = models.CharField(max_length=128, null=True, blank=True)
    address_line_3 = models.CharField(max_length=128, null=True, blank=True)
    city = models.CharField(max_length=128, null=True, blank=True)
    state = models.CharField(max_length=128, null=True, blank=True)
    international_state = models.CharField(max_length=128, null=True,
                                           blank=True)
    postal_code = models.CharField(max_length=128, null=True, blank=True)
    country = models.CharField(max_length=128, null=True, blank=True)
    html_template_name = models.CharField(max_length=1024, null=True,
                                          blank=True)
    text_template_name = models.CharField(max_length=1024, null=True,
                                          blank=True)

    def __unicode__(self):
        return self.name


class SectionTemplate(models.Model):

    name = models.CharField(max_length=255)
    issue_template = models.ForeignKey(IssueTemplate,
                                       related_name='section_templates')
    position = PositionField(collection='issue_template',
                             blank=True)
    categories = models.ManyToManyField(Category,
                                        related_name='section_templates',
                                        null=True,
                                        blank=True)
    content_types = models.ManyToManyField(ContentType,
                                           null=True,
                                           blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('issue_template', 'position')


class AdSize(models.Model):
    name = models.CharField(max_length=128,
                            unique=True)
    height = models.PositiveSmallIntegerField()
    width = models.PositiveSmallIntegerField()

    def __unicode__(self):
        return '{name} ({width}x{height})'.format(
            name=self.name,
            width=self.width,
            height=self.height)


class Ad(models.Model):
    name = models.CharField(max_length=128,
                            unique=True)

    start = models.DateField(null=True,
                             blank=True)
    end = models.DateField(null=True,
                           blank=True)

    size = models.ForeignKey(AdSize)
    url = models.URLField(max_length=255)
    image = models.ImageField(max_length=512,
                              upload_to='django-bulletin/%Y/%m/%d/ad',
                              null=True,
                              blank=True)

    show_on_website = models.BooleanField(default=False)
    include_in_newsletter = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @classmethod
    def ads_for(cls,
                date,
                include_in_newsletter=False,
                show_on_website=False):
        """Return the ads for `date`, for newsletter or website or both.
        """
        ads = cls.objects.all()

        if include_in_newsletter:
            ads.filter(include_in_newsletter=True)

        if show_on_website:
            ads.filter(show_on_website=True)

        ads = ads.filter(start__lte=date).filter(end__gte=date)

        return ads


# class SponsoredPost(models.Model):
#     """Here's one way to do a sponsored post. Another
#     way would be to subclass Post. This SponsoredPost
#     though, is so different from a regular Post, that
#     it seems safe to make it its own thing.

#     'Course, I'm going on vacation now and haven't worked
#     with SponsoredPost yet, so the other way might turn
#     out to be better.


#     """

#     title = models.CharField(max_length=255,
#                              unique=True)
#     url = models.URLField(max_length=255)

#     start = models.DateField(null=True,
#                              blank=True)
#     end = models.DateField(null=True,
#                            blank=True)

#     image = models.ImageField(
#         max_length=512,
#         upload_to='django-bulletin/%Y/%m/%d/sponsored-post',
#         null=True,
#         blank=True)

#     blurb = models.TextField()

#     show_on_website = models.BooleanField(default=False)
#     include_in_newsletter = models.BooleanField(default=False)

#     category = models.ForeignKey(Category,
#                                  related_name='posts',
#                                  null=True,
#                                  blank=True,
#                                  on_delete=models.SET_NULL)

#     class Meta:
#         ordering = ('title')

#     def __unicode__(self):
#         return self.title
