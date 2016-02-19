from braces.views import (LoginRequiredMixin,
                          SetHeadlineMixin,
                          StaffuserRequiredMixin)
from django.conf import settings
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import (CreateView,
                                  DeleteView,
                                  FormView,
                                  ListView,
                                  TemplateView,
                                  UpdateView)
from django.views.generic.base import ContextMixin
from django.views.generic.edit import FormMixin

from .forms import (IssueCreateForm,
                    IssueDeleteForm,
                    IssueSettingsForm,
                    IssueTemplateDeleteForm,
                    IssueTemplateForm,
                    IssueTemplateUpdateSettingsForm,
                    LinkForm,
                    NewsletterForm,
                    NewsletterSubscribeForm,
                    SectionDeleteForm,
                    SectionForm,
                    SectionPostForm,
                    SectionPostRemoveForm,
                    SectionTemplateCategoryAddForm,
                    SectionTemplateCategoryRemoveForm,
                    SectionTemplateDeleteForm,
                    SectionTemplateForm,
                    PostUpdateForm,
                    PostSubmitForm,
                    AdCreateForm,
                    AdUpdateForm,
                    AdDeleteForm)
from .models import (Category,
                     Issue,
                     IssueTemplate,
                     Link,
                     Newsletter,
                     PostCategory,
                     Section,
                     SectionTemplate,
                     Post,
                     Ad)
from tools.plugins.utils import get_active_plugins
from tools.plugins.models import (NewResource,
                                  Opportunity,
                                  Story)


class SidebarView(ContextMixin):
    """A view that loads up the context with info for the
    sidebar.

    Posts are provided in context, as a map indexed by the type
    of Post.  E.g.,

        {'story': [<Story 1>, <Story 2> ...],
         'job': [<Job 1>, <Job 2> ...]
         ...}

    5 most recent (by pub_date) accepted Posts of each type are
    provided, except for Stories. Stories provided are those included
    in the most recently published issue of the newsletter.
    """
    def get_context_data(self, **kwargs):
        context = super(SidebarView, self).get_context_data(**kwargs)

        for plugin in get_active_plugins():
            if plugin.model != 'story':
                plugin_instances = plugin.model_class().objects.filter(
                    approved=True).order_by(
                        '-pub_date', 'title')[:5]
            else:
                plugin_instances = Issue.get_news_from_most_recent_issue()

            context[plugin.model] = plugin_instances

        return context


##############################
# List, CRUD for Newsletter: #
##############################
class NewsletterListView(SetHeadlineMixin,
                         ListView):

    model = Newsletter
    template_name = 'bulletin/newsletter_list.html'
    headline = 'newsletters'


class NewsletterUpdateView(StaffuserRequiredMixin,
                           SetHeadlineMixin,
                           UpdateView):

    model = Newsletter
    form_class = NewsletterForm
    template_name = 'bulletin/newsletter_update.html'
    success_url = reverse_lazy('bulletin:newsletter-list')
    headline = 'update newsletter'

    def get_context_data(self, **kwargs):
        context = super(NewsletterUpdateView, self).get_context_data(
            **kwargs)
        context['newsletter'] = self.get_object()
        return context
####################################
# End of List, CRUD for Newsletter #
####################################


class NewsletterSubscribeView(FormView):

    form_class = NewsletterSubscribeForm
    template_name = 'bulletin/newsletter_subscribe.html'
    success_url_name = 'bulletin:newsletter-subscribe-thanks'

    def get_newsletter(self):
        newsletter = Newsletter.objects.get(pk=self.kwargs['pk'])
        return newsletter

    def form_valid(self, form):
        self.get_newsletter().subscribe(form.cleaned_data['email_address'])
        return super(NewsletterSubscribeView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        return reverse(self.success_url_name, kwargs=self.kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(NewsletterSubscribeView, self).get_context_data(
            *args, **kwargs)
        context['newsletter'] = self.get_newsletter()
        return context


class NewsletterSubscribeThanksView(SidebarView, TemplateView):

    template_name = 'bulletin/newsletter_subscribe_thanks.html'

    def get_newsletter(self):
        newsletter = Newsletter.objects.get(pk=self.kwargs['pk'])
        return newsletter

    def get_context_data(self, *args, **kwargs):
        context = super(NewsletterSubscribeThanksView, self).get_context_data(
            *args, **kwargs)
        context['newsletter'] = self.get_newsletter()
        return context


class NewsletterIssueListView(SetHeadlineMixin,
                              ListView):
    """List the Issues for a Newsletter.
    """
    model = Issue
    template_name = 'bulletin/newsletter_issue_list.html'
    headline = 'issues'

    def get_newsletter(self):
        return Newsletter.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self, *args, **kwargs):
        newsletter = self.get_newsletter()
        return Issue.objects.filter(newsletter=newsletter)

    def get_context_data(self, **kwargs):
        context = super(NewsletterIssueListView, self).get_context_data(
            **kwargs)
        context['newsletter'] = self.get_newsletter()
        return context


###################
# CRUD for Issue: #
###################
class IssueCreateView(StaffuserRequiredMixin,
                      SetHeadlineMixin,
                      CreateView):

    model = Issue
    form_class = IssueCreateForm
    template_name = 'bulletin/issue_create.html'
    headline = 'new issue'

    def get_newsletter(self):
        return Newsletter.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        issue = form.save(commit=False)
        issue.newsletter = self.get_newsletter()
        if form.cleaned_data['issue_template']:
            issue.init_from_issue_template(
                form.cleaned_data['issue_template'])
        return super(IssueCreateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(IssueCreateView, self).get_context_data(
            **kwargs)
        context['newsletter'] = Newsletter.objects.get(pk=self.kwargs['pk'])
        # if user specified next URL on GET, push it into the form so
        # we have it on the POST:
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context

    def get_success_url(self):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:issue-update',
                          kwargs={'pk': self.object.id})
        return url


class IssueUpdateView(StaffuserRequiredMixin,
                      SetHeadlineMixin,
                      UpdateView):

    model = Issue
    template_name = 'bulletin/issue_update.html'
    headline = 'update issue'
    fields = ['name']

    def get_object(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:newsletter-issue-list',
                          kwargs={'pk': self.object.newsletter.id})
        return url

    def get_context_data(self, **kwargs):
        context = super(IssueUpdateView, self).get_context_data(
            **kwargs)
        context['issue'] = self.get_object()
        context['newsletter'] = self.get_object().newsletter
        return context


class IssueSettingsUpdateView(StaffuserRequiredMixin,
                              SetHeadlineMixin,
                              UpdateView):

    model = Issue
    template_name = 'bulletin/issue_settings_update.html'
    headline = 'Update Issue Settings'
    form_class = IssueSettingsForm

    def get_object(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:newsletter-issue-list',
                          kwargs={'pk': self.object.newsletter.id})
        return url

    def get_context_data(self, **kwargs):
        context = super(IssueSettingsUpdateView, self).get_context_data(
            **kwargs)
        context['issue'] = self.get_object()
        context['newsletter'] = self.get_object().newsletter
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context


class IssueDeleteView(StaffuserRequiredMixin,
                      SetHeadlineMixin,
                      DeleteView):
    """Delete an Issue.
    """
    model = Issue
    template_name = 'bulletin/issue_delete.html'
    form_class = IssueDeleteForm

    def get_object(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self, *args, **kwargs):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:newsletter-issue-list',
                          kwargs={'pk': self.get_object().newsletter.id})
        return url

    def get_context_data(self, **kwargs):
        context = super(IssueDeleteView, self).get_context_data(
            **kwargs)
        context['issue'] = self.get_object()
        context['newsletter'] = self.get_object().newsletter
        # if user specified next URL on GET, push it into the form so
        # we have it on the POST:
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context

    def get_headline(self):
        return 'Delete Issue for "{pub_date}"?'.format(
            pub_date=self.get_object().pub_date)
##########################
# End of CRUD for Issue. #
##########################


class IssuePreviewView(TemplateView):
    """Preview what an Issue will look like.
    """
    def get_template_names(self):
        template_name = self.kwargs['template_name']
        return [template_name]

    def get_issue(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(IssuePreviewView, self).get_context_data(
            **kwargs)
        issue = self.get_issue()
        context = issue.get_context_data()
        return context


class ChooseIssuePreviewTypeView(SetHeadlineMixin,
                                 TemplateView):
    """Allow a choice of HTML or text previews of an Issue.
    """
    template_name = 'bulletin/issue_preview.html'
    headline = 'preview an issue'

    def get_issue(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(ChooseIssuePreviewTypeView, self).get_context_data(
            **kwargs)
        context['issue'] = self.get_issue()
        return context


class IssueSectionListView(SetHeadlineMixin,
                           ListView):
    """List the Sections for an Issue.
    """
    model = Section
    template_name = 'bulletin/issue_section_list.html'
    headline = 'issue sections'

    def get_issue(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self, *args, **kwargs):
        issue = self.get_issue()
        return Section.objects.filter(issue=issue).order_by('position')

    def get_context_data(self, **kwargs):
        context = super(IssueSectionListView, self).get_context_data(
            **kwargs)
        context['issue'] = self.get_issue()
        context['newsletter'] = self.get_issue().newsletter
        return context


#####################
# CRUD for Section: #
#####################
class SectionCreateView(StaffuserRequiredMixin,
                        SetHeadlineMixin,
                        CreateView):

    model = Section
    form_class = SectionForm
    template_name = 'bulletin/section_create.html'
    headline = 'create a section'

    def get_issue(self):
        return Issue.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        issue = self.get_issue()
        section = form.save(commit=False)
        section.issue = issue
        return super(SectionCreateView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:section-update',
                          kwargs={'pk': self.object.id})
        return url

    def get_context_data(self, **kwargs):
        context = super(SectionCreateView, self).get_context_data(
            **kwargs)
        # issue and newsletter for breadcrumbs:
        context['issue'] = self.get_issue()
        context['newsletter'] = self.get_issue().newsletter
        # if user specified next URL on GET, push it into the form so
        # we have it on the POST:
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context


class SectionUpdateView(StaffuserRequiredMixin,
                        SetHeadlineMixin,
                        UpdateView):

    model = Section
    form_class = SectionForm
    template_name = 'bulletin/section_update.html'
    headline = 'update section'

    def get_success_url(self, *args, **kwargs):
        return reverse('bulletin:issue-section-list',
                       kwargs={'pk': self.object.issue.id})

    def get_context_data(self, **kwargs):
        context = super(SectionUpdateView, self).get_context_data(**kwargs)
        context['section'] = self.get_object()
        context['issue'] = self.get_object().issue
        context['newsletter'] = self.get_object().issue.newsletter
        return context

    def get_object(self):
        return Section.objects.get(pk=self.kwargs['pk'])


class SectionDeleteView(StaffuserRequiredMixin,
                        SetHeadlineMixin,
                        DeleteView):
    """Delete a Section.
    """
    model = Section
    template_name = 'bulletin/section_delete.html'
    form_class = SectionDeleteForm

    def get_object(self):
        return Section.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self, *args, **kwargs):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:issue-section-list',
                          kwargs={'pk': self.object.issue.id})
        return url

    def get_context_data(self, **kwargs):
        context = super(SectionDeleteView, self).get_context_data(
            **kwargs)
        context['issue'] = self.get_object().issue
        context['newsletter'] = self.get_object().issue.newsletter
        # if user specified next URL on GET, push it into the form so
        # we have it on the POST:
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context

    def get_headline(self):
        return 'Delete Section "{name}"?'.format(
            name=self.get_object().name)
############################
# End of CRUD for Section. #
############################


class SectionPostListView(SetHeadlineMixin,
                          ListView):
    """List the Posts in a Section.
    """
    model = Post
    template_name = 'bulletin/section_post_list.html'
    headline = 'section posts'

    def get_section(self):
        return Section.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self, *args, **kwargs):
        section = self.get_section()
        return Post.objects.filter(section=section)

    def get_context_data(self, **kwargs):
        context = super(SectionPostListView, self).get_context_data(
            **kwargs)
        context['section'] = self.get_section()
        context['issue'] = self.get_section().issue
        context['newsletter'] = self.get_section().issue.newsletter
        return context


class SectionPostAddView(StaffuserRequiredMixin,
                         SetHeadlineMixin,
                         UpdateView):
    """Add a Post to a Section.
    """
    model = Section
    form_class = SectionPostForm
    template_name = 'bulletin/section_post_add.html'
    headline = 'Add a post'

    def form_valid(self, form):
        selected_posts = form.cleaned_data['available_posts']
        if selected_posts:
            for post in selected_posts:
                post.section = self.object
                post.save()
        return super(SectionPostAddView, self).form_valid(form)

    def get_object(self):
        return Section.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self, *args, **kwargs):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:section-post-list',
                          kwargs={'pk': self.get_object().id})
        return url

    def get_context_data(self, **kwargs):
        context = super(SectionPostAddView, self).get_context_data(
            **kwargs)
        context['section'] = self.get_object()
        context['issue'] = self.get_object().issue
        context['newsletter'] = self.get_object().issue.newsletter
        # if user specified next URL on GET, push it into the form so
        # we have it on the POST:
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context


class SectionPostRemoveView(StaffuserRequiredMixin,
                            SetHeadlineMixin,
                            DeleteView):
    """Remove a Post from a Section.

    Note that though this is a DeleteView, and it's model is Section,
    no Section is ever deleted.  The only thing that gets deleted is
    the link between the post and the section.
    """
    model = Section
    template_name = 'bulletin/section_post_remove.html'
    form_class = SectionPostRemoveForm

    def get_post(self):
        return Post.objects.get(pk=self.kwargs['post_pk'])

    def delete(self, request, *args, **kwargs):
        section = self.get_object()
        post = self.get_post()
        section.posts.remove(post)
        section.save()
        return redirect(self.get_success_url())

    def get_object(self):
        return Section.objects.get(pk=self.kwargs['section_pk'])

    def get_success_url(self, *args, **kwargs):
        return reverse('bulletin:section-post-list',
                       kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super(SectionPostRemoveView, self).get_context_data(
            **kwargs)
        context['post'] = self.get_post()
        context['section'] = self.get_object()
        context['issue'] = self.get_object().issue
        context['newsletter'] = self.get_object().issue.newsletter
        return context

    def get_headline(self):
        return 'Remove post "{title}"?'.format(
            title=self.get_post().title.strip())


class FrontPageView(SetHeadlineMixin,
                    ListView):

    model = Post
    queryset = Post.objects.filter(approved=True).order_by('-pub_date')
    template_name = 'bulletin/front_page.html'
    paginate_by = settings.NUM_POSTS_ON_FRONT_PAGE
    headline = 'All Posts'


class PostListView(SetHeadlineMixin,
                   ListView,
                   SidebarView):

    paginate_by = settings.NUM_POSTS_ON_FRONT_PAGE

    def get_queryset(self, *args, **kwargs):
        model = getattr(self, 'model', Post)
        queryset = model.objects.filter(approved=True).order_by('-pub_date',
                                                                'title')
        category_id = self.request.GET.get('category')
        if category_id:
            category = get_object_or_404(Category, pk=category_id)
            queryset = queryset.filter(categories__in=[category])

        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)

        context['categories'] = Category.objects.all().order_by('name')

        category_id = self.request.GET.get('category')
        if category_id:
            context['current_filter_name'] = Category.objects.get(
                pk=category_id).name
        else:
            context['current_filter_name'] = 'All'

        return context


#######################
# CRUD for Post:      #
#######################
def get_max_post_title_length(queryset):
    model = queryset.model
    if model == Story:
        return getattr(settings, 'MAX_STORY_TITLE_LENGTH', -1)
    else:
        return -1


def get_max_post_blurb_length(queryset):
    model = queryset.model

    if model == Story:
        return getattr(settings, 'MAX_STORY_BLURB_LENGTH', -1)
    elif model == Opportunity:
        return getattr(settings, 'MAX_OPPORTUNITY_BLURB_LENGTH', -1)
    elif model == NewResource:
        return getattr(settings, 'MAX_NEW_RESOURCE_BLURB_LENGTH', -1)
    else:
        return -1


class PostFormMixin(FormMixin):

    def form_valid(self, form):
        categories = form.cleaned_data.pop('categories')

        try:
            primary_category = form.cleaned_data.pop('primary_category')[0]
        except (KeyError, IndexError):
            primary_category = None

        self.object = form.save(commit=False)
        self.object.save()

        self.object.categories.clear()

        for category in categories:
            PostCategory.objects.create(post=self.object,
                                        category=category,
                                        primary=False)

        if primary_category:
            post_category, _ = PostCategory.objects.get_or_create(
                post=self.object,
                category=primary_category)
            if not post_category.primary:
                post_category.primary = True
                post_category.save()

        return super(PostFormMixin, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(PostFormMixin, self).get_context_data(
            **kwargs)

        queryset = self.get_queryset()
        context['max_post_title_length'] = get_max_post_title_length(queryset)
        context['max_post_blurb_length'] = get_max_post_blurb_length(queryset)

        context['next'] = self.request.GET.get('next', '')

        return context


class PostSubmitView(LoginRequiredMixin,
                     SetHeadlineMixin,
                     PostFormMixin,
                     CreateView):
    form_class = PostSubmitForm
    model = Post
    template_name = 'bulletin/submit_post.html'
    headline = 'Submit a Post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.submitter = self.request.user
        return super(PostSubmitView, self).form_valid(form)

    def get_success_url(self):
        return '{url}?next={next}'.format(
            url=reverse('bulletin:thanks-for-submitting-post'),
            next=self.request.POST.get('next') or '/')

    def get_context_data(self, **kwargs):
        context = super(PostSubmitView, self).get_context_data(
            **kwargs)

        context['screen_image_uploads'] = getattr(settings,
                                                  'SCREEN_IMAGE_UPLOADS',
                                                  False)
        context['screen_image_license_text'] = getattr(
            settings,
            'SCREEN_IMAGE_LICENSE_TEXT',
            'You should set SCREEN_IMAGE_LICENSE_TEXT in settings.py.')

        return context


class PostUpdateView(StaffuserRequiredMixin,
                     SetHeadlineMixin,
                     PostFormMixin,
                     UpdateView):

    form_class = PostUpdateForm
    model = Post
    template_name = 'bulletin/post_update.html'
    headline = 'update post'
    query_string = True

    def get_post(self):
        return Post.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return self.request.POST['next']

    def get_context_data(self, **kwargs):
        context = super(PostUpdateView, self).get_context_data(
            **kwargs)

        context['post'] = self.get_post()

        return context


######################
# End of Post CRUD. #
######################


class PostLinkListView(SetHeadlineMixin,
                       ListView):
    """List all the Links for a Post.
    """
    model = Link

    template_name = 'bulletin/post_link_list.html'
    headline = 'post links'

    def get_post(self):
        return Post.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        return Link.objects.filter(post=self.get_post())

    def get_success_url(self):
        return self.request.POST['next']

    def get_context_data(self, **kwargs):
        context = super(PostLinkListView, self).get_context_data(
            **kwargs)
        context['post'] = self.get_post()
        context['next'] = self.request.GET['next']
        return context


class ThankYouForSubmittingPostView(TemplateView,
                                    SetHeadlineMixin):
    """Say, "Thanks" after someone submits a post.
    """

    template_name = 'bulletin/thank_you_for_submitting_post.html'

    def get_context_data(self, **kwargs):
        context = super(ThankYouForSubmittingPostView,
                        self).get_context_data(**kwargs)
        context['next'] = self.request.GET['next']
        return context


######################
# CRUD for Link:     #
######################
class LinkCreateView(StaffuserRequiredMixin,
                     SetHeadlineMixin,
                     CreateView):

    model = Link
    form_class = LinkForm
    headline = 'new post link'
    template_name = 'bulletin/link.html'

    def get_post(self):
        return Post.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return self.request.POST['next']

    def get_context_data(self, **kwargs):
        context = super(LinkCreateView, self).get_context_data(
            **kwargs)
        context['post'] = self.get_post()
        context['next'] = self.request.GET['next']
        return context

    def form_valid(self, form):
        link = form.save(commit=False)
        link.post = self.get_post()
        return super(LinkCreateView, self).form_valid(form)


class LinkUpdateView(StaffuserRequiredMixin,
                     SetHeadlineMixin,
                     UpdateView):

    model = Link
    form_class = LinkForm
    headline = 'update post link'
    template_name = 'bulletin/link.html'

    def get_success_url(self):
        return self.request.POST['next']

    def get_context_data(self, **kwargs):
        context = super(LinkUpdateView, self).get_context_data(
            **kwargs)
        context['link'] = self.get_object()
        context['next'] = self.request.GET['next']
        return context


#####################
# End of Link CRUD. #
#####################


###########################
# CRUD for IssueTemplate: #
###########################
class IssueTemplateCreateView(StaffuserRequiredMixin,
                              SetHeadlineMixin,
                              CreateView):

    model = IssueTemplate
    form_class = IssueTemplateForm
    template_name = 'bulletin/section_template_create.html'
    headline = 'new issue template'

    def get_newsletter(self):
        return Newsletter.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        newsletter = self.get_newsletter()
        issue_template = form.save(commit=False)
        issue_template.newsletter = newsletter
        return super(IssueTemplateCreateView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        if ('next' in self.request.POST and
            self.request.POST['next']):
            return self.request.POST['next']
        return reverse('bulletin:newsletter-issue-template-list',
                       kwargs={'pk': self.get_newsletter().id})

    def get_context_data(self, **kwargs):
        context = super(IssueTemplateCreateView, self).get_context_data(
            **kwargs)
        context['newsletter'] = self.get_newsletter()
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context


class IssueTemplateUpdateView(StaffuserRequiredMixin,
                              SetHeadlineMixin,
                              UpdateView):

    form_class = IssueTemplateForm
    model = IssueTemplate
    template_name = 'bulletin/issue_template_update.html'
    headline = 'update issue template'

    def get_newsletter(self):
        return self.get_object().newsletter

    def get_success_url(self):
        if ('next' in self.request.POST and
            self.request.POST['next']):
            return self.request.POST['next']
        return reverse('bulletin:newsletter-issue-template-list',
                       kwargs={'pk': self.get_newsletter().id})

    def get_context_data(self, **kwargs):
        context = super(IssueTemplateUpdateView, self).get_context_data(
            **kwargs)
        context['issue_template'] = self.get_object()
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context


class IssueTemplateSettingsUpdateView(StaffuserRequiredMixin,
                                      SetHeadlineMixin,
                                      UpdateView):
    """An update view for just the settings of an IssueTemplate.
    """
    form_class = IssueTemplateUpdateSettingsForm
    model = IssueTemplate
    template_name = 'bulletin/issue_template_settings_update.html'
    headline = 'update issue template settings'

    def get_newsletter(self):
        return self.get_object().newsletter

    def get_success_url(self):
        if ('next' in self.request.POST and
            self.request.POST['next']):
            return self.request.POST['next']
        return reverse('bulletin:newsletter-issue-template-list',
                       kwargs={'pk': self.get_newsletter().id})

    def get_context_data(self, **kwargs):
        context = super(IssueTemplateSettingsUpdateView,
                        self).get_context_data(**kwargs)
        context['issue_template'] = self.get_object()
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context


class IssueTemplateDeleteView(StaffuserRequiredMixin,
                              SetHeadlineMixin,
                              DeleteView):
    """Delete a IssueTemplate.
    """
    model = IssueTemplate
    template_name = 'bulletin/item_template_delete.html'
    form_class = IssueTemplateDeleteForm

    def get_success_url(self, *args, **kwargs):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:newsletter-issue-template-list',
                          kwargs={'pk': self.object.newsletter.id})
        return url

    def get_context_data(self, **kwargs):
        context = super(IssueTemplateDeleteView, self).get_context_data(
            **kwargs)
        context['issue_template'] = self.object
        context['newsletter'] = self.object.newsletter
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context

    def get_headline(self):
        return 'delete issue template "{name}"?'.format(
            name=self.get_object().name)
##############################
# End of IssueTemplate CRUD. #
##############################


class NewsletterIssueTemplateListView(SetHeadlineMixin,
                                      ListView):
    """List the IssueTemplates for a Newsletter.
    """
    model = IssueTemplate
    template_name = 'bulletin/newsletter_issue_template_list.html'
    headline = 'issue templates'

    def get_newsletter(self):
        return Newsletter.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self, *args, **kwargs):
        newsletter = self.get_newsletter()
        return IssueTemplate.objects.filter(newsletter=newsletter)

    def get_context_data(self, **kwargs):
        context = super(NewsletterIssueTemplateListView,
                        self).get_context_data(**kwargs)
        context['newsletter'] = self.get_newsletter()
        return context


#############################
# CRUD for SectionTemplate: #
#############################
class SectionTemplateCreateView(StaffuserRequiredMixin,
                                SetHeadlineMixin,
                                CreateView):

    model = SectionTemplate
    form_class = SectionTemplateForm
    template_name = 'bulletin/section_template_create.html'
    headline = 'new section template'

    def get_issue_template(self):
        return IssueTemplate.objects.get(pk=self.kwargs['pk'])

    def form_valid(self, form):
        issue_template = self.get_issue_template()
        section_template = form.save(commit=False)
        section_template.issue_template = issue_template
        return super(SectionTemplateCreateView, self).form_valid(form)

    def get_success_url(self, *args, **kwargs):
        if 'next' in self.request.POST:
            return self.request.POST['next']
        return reverse('bulletin:section-template-update',
                       kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(SectionTemplateCreateView, self).get_context_data(
            **kwargs)
        context['issue_template'] = self.get_issue_template()
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context


class SectionTemplateUpdateView(StaffuserRequiredMixin,
                                SetHeadlineMixin,
                                UpdateView):

    form_class = SectionTemplateForm
    model = SectionTemplate
    template_name = 'bulletin/section_template_update.html'
    headline = 'update section template'

    def get_section_template(self):
        return SectionTemplate.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        return self.request.POST['next']

    def get_context_data(self, **kwargs):
        context = super(SectionTemplateUpdateView, self).get_context_data(
            **kwargs)
        context['section_template'] = self.get_section_template()
        context['next'] = self.request.GET['next']
        return context


class SectionTemplateDeleteView(StaffuserRequiredMixin,
                                SetHeadlineMixin,
                                DeleteView):
    """Delete a SectionTemplate.
    """
    model = SectionTemplate
    template_name = 'bulletin/section_demplate_delete.html'
    form_class = SectionTemplateDeleteForm

    def get_object(self):
        return SectionTemplate.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self, *args, **kwargs):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:issue-section-template-list',
                          kwargs={'pk': self.object.issue.id})
        return url

    def get_context_data(self, **kwargs):
        context = super(SectionTemplateDeleteView, self).get_context_data(
            **kwargs)
        context['issue_template'] = self.get_object().issue_template
        context['section_template'] = self.get_object()
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context

    def get_headline(self):
        return 'Delete Section "{name}"?'.format(
            name=self.get_object().name)
################################
# End of SectionTemplate CRUD. #
################################


class IssueTemplateSectionTemplateListView(SetHeadlineMixin,
                                           ListView):
    """List all the SectionTemplates for an IssueTemplate.
    """
    model = SectionTemplate

    template_name = 'bulletin/issue_template_section_template_list.html'
    headline = 'issue template sections'

    def get_issue_template(self):
        return IssueTemplate.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        return SectionTemplate.objects.filter(
            issue_template=self.get_issue_template())

    def get_context_data(self, **kwargs):
        context = super(IssueTemplateSectionTemplateListView,
                        self).get_context_data(**kwargs)
        context['issue_template'] = self.get_issue_template()
        try:
            context['next'] = self.request.GET['next']
        except KeyError:
            pass
        return context


class SectionTemplateCategoryListView(SetHeadlineMixin,
                                      ListView):
    """List all the Categories for a SectionTemplate.
    """
    model = Category

    template_name = 'bulletin/section_template_category_list.html'
    headline = 'section categories'

    def get_section_template(self):
        return SectionTemplate.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        return Category.objects.filter(
            section_template=self.get_section_template())

    def get_context_data(self, **kwargs):
        context = super(SectionTemplateCategoryListView,
                        self).get_context_data(**kwargs)
        context['section_template'] = self.get_section_template()
        try:
            context['next'] = self.request.GET['next']
        except KeyError:
            pass
        return context


class SectionTemplateCategoryAddView(StaffuserRequiredMixin,
                                     SetHeadlineMixin,
                                     UpdateView):
    """Add a Category to a SectionTemplate.
    """
    model = SectionTemplate
    form_class = SectionTemplateCategoryAddForm
    template_name = 'bulletin/section_template_category_add.html'
    headline = 'add a category'

    def form_valid(self, form):
        selected_categories = form.cleaned_data['unsectioned_categories']
        if selected_categories:
            for category in selected_categories:
                self.object.categories.add(category)
        return super(SectionTemplateCategoryAddView, self).form_valid(form)

    def get_object(self):
        return SectionTemplate.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self, *args, **kwargs):
        if ('next' in self.request.POST and
            self.request.POST['next']):
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:section-template-category-list',
                          kwargs={'pk': self.object.id})
        return url

    def get_context_data(self, **kwargs):
        context = super(SectionTemplateCategoryAddView,
                        self).get_context_data(**kwargs)
        context['unsectioned_categories'] = Category.objects.filter(
            section_templates=None)
        # section_templates does not include SectionTemplate with
        # SectionTemplate.IssueTemplate == self.issue_template)

        context['section_template'] = self.get_object()
        context['issue_template'] = self.get_object().issue_template
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context


class SectionTemplateCategoryRemoveView(StaffuserRequiredMixin,
                                        SetHeadlineMixin,
                                        DeleteView):
    """Remove a Category from a SectionTemplate.

    Note that though this is a DeleteView, and it's model is SectionTemplate,
    no SectionTemplate is ever deleted.  The only thing that gets deleted is
    the link between the category and the section template.
    """
    model = SectionTemplate
    template_name = 'bulletin/section_template_category_remove.html'
    form_class = SectionTemplateCategoryRemoveForm

    def get_category(self):
        return Category.objects.get(pk=self.kwargs['category_pk'])

    def delete(self, request, *args, **kwargs):
        section_template = self.get_object()
        category = self.get_category()
        section_template.categories.remove(category)
        section_template.save()
        return redirect(self.get_success_url())

    def get_object(self):
        return SectionTemplate.objects.get(
            pk=self.kwargs['section_template_pk'])

    def get_success_url(self, *args, **kwargs):
        return reverse('bulletin:section-template-category-list',
                       kwargs={'pk': self.get_object().id})

    def get_context_data(self, **kwargs):
        context = super(SectionTemplateCategoryRemoveView,
                        self).get_context_data(**kwargs)
        context['category'] = self.get_category()
        context['section_template'] = self.get_object()
        return context

    def get_headline(self):
        return 'Remove category "{name}"?'.format(
            name=self.get_category().name.strip())


class UnmoderatedPostListView(SetHeadlineMixin,
                              ListView):

    model = Post
    queryset = Post.objects.filter(approved=None).order_by('date_submitted')
    template_name = 'bulletin/unmoderated_post_list.html'
    headline = 'unmoderated posts'


class AlternativeIssueEditor(TemplateView):
    """AlternativeIssueEditor is the react-or-jstree-based one.

    It doesn't work.

    Yet . . .
    """
    template_name = 'bulletin/alternative_issue_editor.html'


################
# CRUD for Ad: #
################
class AdListView(SetHeadlineMixin,
                 ListView):
    """List Ads.
    """
    model = Ad
    template_name = 'bulletin/ad_list.html'
    headline = 'ads'


class AdCreateView(StaffuserRequiredMixin,
                   SetHeadlineMixin,
                   CreateView):

    model = Ad
    form_class = AdCreateForm
    template_name = 'bulletin/ad_create.html'
    headline = 'new ad'

    def get_newsletter(self):
        return Newsletter.objects.get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super(AdCreateView, self).get_context_data(
            **kwargs)
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context

    def get_success_url(self):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:ad-list')
        return url


class AdUpdateView(StaffuserRequiredMixin,
                   SetHeadlineMixin,
                   UpdateView):

    model = Ad
    template_name = 'bulletin/ad_update.html'
    headline = 'update ad'
    form_class = AdUpdateForm

    def get_object(self):
        return Ad.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        if self.request.POST.get('next'):
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:ad-list')
        return url

    def get_context_data(self, **kwargs):
        context = super(AdUpdateView, self).get_context_data(
            **kwargs)
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context


class AdDeleteView(StaffuserRequiredMixin,
                   SetHeadlineMixin,
                   DeleteView):
    """Delete an Ad.
    """
    model = Ad
    template_name = 'bulletin/ad_delete.html'
    form_class = AdDeleteForm

    def get_object(self):
        return Ad.objects.get(pk=self.kwargs['pk'])

    def get_success_url(self, *args, **kwargs):
        if 'next' in self.request.POST:
            url = self.request.POST['next']
        else:
            url = reverse('bulletin:ad-list')
        return url

    def get_context_data(self, **kwargs):
        context = super(AdDeleteView, self).get_context_data(
            **kwargs)
        context['ad'] = self.get_object()
        # if user specified next URL on GET, push it into the form so
        # we have it on the POST:
        if 'next' in self.request.GET:
            context['next'] = self.request.GET['next']
        return context

    def get_headline(self):
        return 'Delete Ad "{name}"?'.format(
            name=self.get_object().name)
#######################
# End of CRUD for Ad. #
#######################
