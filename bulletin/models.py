from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.contrib.contenttypes.models import ContentType
from django.db import models, transaction
from django.template.response import SimpleTemplateResponse
from django.utils import timezone

import polymorphic.models

from django_constant_contact.models import EmailMarketingCampaign
from positions.fields import PositionField
from python_constantcontact import cc


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
                                blank=True,
                                db_index=True)
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
        return response.content.decode('utf-8')

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

    @classmethod
    def get_most_recently_published_issue(cls):
        """Returns the Issue that was most recently published.
        If no issue has been published, returns None.
        """
        for issue in cls.objects.order_by('-pub_date'):
            if issue.pub_date is None:
                continue
            if issue.pub_date > timezone.now().date():  # Fear the timezone!
                continue
            return issue

        return None

    @classmethod
    def get_news_from_most_recent_issue(cls):
        """Returns the news stories from the most recently published
        issue of the newsletter.
        """
        issue = cls.get_most_recently_published_issue()

        news_section = None
        if issue:
            for section in issue.sections.all():
                if section.name.lower() == "news":
                    news_section = section
                    break

        if news_section:
            news_stories = news_section.posts.order_by('-pub_date')
        else:
            news_stories = None

        return news_stories  # Will be empty before 1st issue is published.

    @property
    def posts(self):
        """Returns a list of all Posts in this Issue.
        """
        posts = []
        for section in self.sections.all():
            posts += section.posts.all()
        return posts


class Category(models.Model):

    name = models.CharField(max_length=255,
                            db_index=True)
    parent = models.ForeignKey("self",
                               null=True,
                               blank=True)
    fully_qualified_name = models.CharField(max_length=1024,
                                            null=True,
                                            blank=True,
                                            db_index=True)
    private = models.BooleanField(default=False,
                                  blank=True)
    image = models.ImageField(max_length=512,
                              upload_to='django-bulletin/%Y/%m/%d/category',
                              null=True,
                              blank=True)
    url = models.URLField(max_length=1024,
                          null=True,
                          blank=True)

    class Meta:
        ordering = ['fully_qualified_name']
        verbose_name_plural = 'categories'
        index_together = ['parent', 'name']

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

    name = models.CharField(max_length=255,
                            db_index=True)
    issue = models.ForeignKey(Issue,
                              related_name='sections')
    position = models.IntegerField(null=True,
                                   blank=True)
    categories = models.ManyToManyField(Category,
                                        related_name='sections',
                                        blank=True)
    content_types = models.ManyToManyField(ContentType,
                                           blank=True)

    class Meta:
        ordering = ('issue', 'position')
        index_together = ['issue', 'position']

    def __unicode__(self):
        return "{issue}: {section_name}".format(
            issue=self.issue, section_name=self.name)

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

    def fix_post_positions(self):
        """Ensures that the positions of all Posts in this Section
        are sequential, starting at 1.
        """
        for position, post in enumerate(self.posts.all().order_by('position'), start=1):
            if post.position != position:
                post.position = position
                post.save()

    def save(self, *args, **kwargs):
        if self.issue and self.position is None:
            self.position = self.issue.sections.count() + 1
        elif self.issue is None:
            self.position = None
        return super(Section, self).save(*args, **kwargs)


class Post(polymorphic.models.PolymorphicModel):

    date_submitted = models.DateTimeField(auto_now_add=True,
                                          db_index=True)
    # Required fields:
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=1024)
    submitter = models.ForeignKey(User)
    # Optional fields:
    approved = models.NullBooleanField(null=True,
                                       db_index=True)
    include_in_newsletter = models.BooleanField(default=True,
                                                blank=True,
                                                db_index=True)
    feature = models.BooleanField(default=False,
                                  blank=True,
                                  db_index=True)
    pub_date = models.DateTimeField(blank=True,
                                    null=True,
                                    db_index=True)
    categories = models.ManyToManyField(Category,
                                        through='PostCategory',
                                        related_name='posts',
                                        blank=True)
    section = models.ForeignKey(Section,
                                related_name='posts',
                                null=True,
                                blank=True,
                                on_delete=models.SET_NULL)
    position = models.IntegerField(null=True,
                                   blank=True,
                                   db_index=True)
    image = models.ImageField(max_length=512,
                              upload_to='django-bulletin/%Y/%m/%d/post',
                              null=True,
                              blank=True)
    cloned_from = models.ForeignKey('self',
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
                                              section=None).order_by(
                                                  '-feature', 'title')
        return available_posts

    def __unicode__(self):
        return self.title

    def up(self):
        if self.section.posts.filter(position=self.position).count() > 1:
            self.section.fix_post_positions()

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
        if self.section.posts.filter(position=self.position).count() > 1:
            self.section.fix_post_positions()

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

    @property
    def primary_category(self):
        try:
            return PostCategory.objects.filter(post=self,
                                               primary=True).first().category
        except AttributeError:  # Is the the correct Error to catch?
            return None

    @primary_category.setter
    def primary_category(self, category):
        current_primary_post_category = PostCategory.objects.filter(
            post=self, primary=True).first()
        if current_primary_post_category:
            current_primary_post_category.primary = False
            current_primary_post_category.save()
        try:
            new_primary_post_category = PostCategory.objects.get(
                post=self, category=category)
        except PostCategory.DoesNotExist:
            new_primary_post_category = PostCategory.objects.create(
                post=self, category=category, primary=True)
        else:
            new_primary_post_category.primary = True
        new_primary_post_category.save()

    def save(self, *args, **kwargs):
        if self.approved and not self.pub_date:
            self.pub_date = timezone.now()
        if self.section and self.position is None:
            self.position = self.section.posts.count() + 1
        elif self.section is None:
            self.position = None
        return super(Post, self).save(*args, **kwargs)

    def clone(self, new_post=None):
        new_post = new_post or Post()
        new_post.date_submitted = self.date_submitted
        new_post.title = self.title
        new_post.url = self.url
        new_post.submitter = self.submitter
        new_post.approved = self.approved
        new_post.include_in_newsletter = self.include_in_newsletter
        new_post.feature = self.feature
        new_post.pub_date = timezone.now()
        new_post.image = self.image
        new_post.cloned_from = self
        new_post.save()
        for post_category in PostCategory.objects.filter(
                category__in=self.categories.all()).filter(
                    post_id=self.id):
            PostCategory.objects.create(post=new_post,
                                        category=post_category.category,
                                        primary=post_category.primary)
        return new_post


class PostCategory(models.Model):

    class Meta:
        ordering = ('post', '-primary')
        index_together = ['post', 'category']

    post = models.ForeignKey(Post)
    category = models.ForeignKey(Category)
    primary = models.BooleanField(default=False)


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
                                        blank=True)
    content_types = models.ManyToManyField(ContentType,
                                           blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('issue_template', 'position')
        index_together = ['issue_template', 'position']


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
                             blank=True,
                             db_index=True)
    end = models.DateField(null=True,
                           blank=True,
                           db_index=True)

    size = models.ForeignKey(AdSize)
    url = models.URLField(max_length=1024)
    image = models.ImageField(max_length=512,
                              upload_to='django-bulletin/%Y/%m/%d/ad',
                              null=True,
                              blank=True)

    show_on_website = models.BooleanField(default=False,
                                          db_index=True)
    include_in_newsletter = models.BooleanField(default=False,
                                                db_index=True)

    display_weight = models.SmallIntegerField(
        default=1,
        help_text="Ads appear in ascending order of Display Weight",
        db_index=True)

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

        ads = ads.filter(start__lte=date).filter(end__gte=date).order_by(
            "display_weight")

        return ads


class ScheduledPost(models.Model):

    post = models.ForeignKey(Post)
    pub_date = models.DateField(db_index=True)

    def make_available_to_issue(self, issue):
        """Make this Post available to `issue`, unless it's already in
        `issue`.

        A Post is available for an issue if it's approved, marked for
        inclusion in the newsletter, and not already in an Issue.

        Note that the Post created is not linked to `issue` here.  That
        happens when `issue` is filled via the 'issue-fill' API endpoint.
        """
        if self.post in [post.cloned_from for post in issue.posts]:
            # A clone of this Post is already in `issue`.
            return None
        cloned_post = self.post.clone()
        cloned_post.pub_date = issue.pub_date
        cloned_post.save()
        return cloned_post

    @classmethod
    def make_all_available_to_issue(cls, issue):
        """Make all ScheduledPosts scheduled to be published on
        `issue`.pub_date available for inclusion in `issue`.
        """
        available_posts = []
        for scheduled_post in cls.objects.filter(pub_date=issue.pub_date):
            post = scheduled_post.make_available_to_issue(issue)
            if post:
                available_posts.append(post)
        return available_posts

    def is_published(self):
        return Post.objects.filter(cloned_from=self.post).count() > 0
