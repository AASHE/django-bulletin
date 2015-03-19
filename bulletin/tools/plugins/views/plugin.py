import braces.views
import django.core.urlresolvers
import django.shortcuts
import django.views.generic

from bulletin.views import SidebarView
from bulletin.tools.plugins.forms import plugin as forms
from bulletin.tools.plugins.utils import get_active_plugins


class PluginSubmitView(braces.views.LoginRequiredMixin,
                       braces.views.SetHeadlineMixin,
                       django.views.generic.FormView):
    """Allow user to select one of the installed plugin types,
    then redirect to the submission form for that type of Post.
    """
    template_name = 'plugins/choose_post_type.html'
    headline = 'Which type of Post?'
    form_class = forms.ChoosePostTypeForm

    def form_valid(self, form):
        selected_type = form.cleaned_data['post_types']
        type_url = django.core.urlresolvers.reverse(
            'bulletin:plugins:{selected_type}-submit'.format(
                selected_type=selected_type))
        return django.shortcuts.redirect(type_url)


class PluginUpdateView(braces.views.LoginRequiredMixin,
                       braces.views.SetHeadlineMixin,
                       django.views.generic.RedirectView):
    """An UpdateView that dispatches to an update view
    specific to the type of Post specified.
    """
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        post_type = kwargs['post_type']
        url = django.core.urlresolvers.reverse(
            'bulletin:plugins:{post_type}-update'.format(
                post_type=post_type),
            kwargs={'pk': kwargs['pk']})
        next_page = self.request.GET.get('next')
        if next_page:
            url += '?next={next}'.format(next=next_page)
        return url


class PluginListView(SidebarView,
                     braces.views.SetHeadlineMixin,
                     django.views.generic.TemplateView):
    """List the installed plugins.
    """
    template_name = 'plugins/plugin_list.html'
    headline = 'Submissions'

    def get_context_data(self, *args, **kwargs):
        context = super(PluginListView, self).get_context_data(*args, **kwargs)
        context['post_types'] = [
            {'name': 'News',
             'description': (
                 """
                 News submitted should be directly relevant to higher education
                 sustainability. The publication date of the news release or
                 article cannot be older than two months from date of
                 submission.
                 """),
             'button_caption': 'Submit a News Story',
             'submit_url': django.core.urlresolvers.reverse(
                 'bulletin:plugins:story-submit')},
            {'name': 'Opportunities',
             'description': (
                 """
                 Opportunities for the campus sustainability
                 community. We welcoms submissions on a national,
                 regional and local level. Surveys directly related to
                 research on campus sustainability - both announcements
                 of such surveys as well as results available online -
                 will be considered for publication. Jobs, as well as
                 internships and fellowships, should not be submitted
                 as Opportunities; they should be submitted as Jobs.
                 """),
             'button_caption': 'Submit an Opportunity',
             'submit_url': django.core.urlresolvers.reverse(
                 'bulletin:plugins:opportunity-submit')},
            {'name': 'New Resources',
             'description': (
                 """
                 Recently published resources. Examples include
                 campus sustainability reports; campus sustainability focused
                 white papers; new magazines or journals; websites or
                 newsletters focused on campus sustainability; and campus
                 sustainability videos. New resources should be accessible
                 to the higher education sustainability community at large.
                 """),
             'button_caption': 'Submit a New Resource',
             'submit_url': django.core.urlresolvers.reverse(
                 'bulletin:plugins:new-resource-submit')},
            {'name': 'Events',
             'description': (
                 """
                 Events should involve significant participation beyond the
                 city or state/province, and should be focused on higher
                 education sustainability or have a major track clearly
                 dedicated to higher education.
                 """),
             'button_caption': 'Submit an Event',
             'submit_url': django.core.urlresolvers.reverse(
                 'bulletin:plugins:event-submit')},
            {'name': 'Jobs',
             'description': (
                 """
                 Job postings are free for member organizations.
                 Jobs should be directly related to furthering campus
                 sustainability (faculty positions in a
                 sustainability-related field can be included) and have
                 sustainability concepts as part of their job descriptions.

                 Jobs are included on the Bulletin website and in one
                 issue of the newsletter.

                 Internships and fellowships should be submitted as Jobs,
                 not as Opportunities.

                 We do not include job opportunities available to
                 students/faculty/staff at only one school, or programs that
                 are not new programs but are just seeking graduates. That's
                 what our ads are for. If you are interested in advertising
                 through the AASHE Bulletin, contact Skyelar Habberfield
                 at <a href="mailto:skyelar.habberfield@aashe.org">
                 skyelar.habberfield@aashe.org</a>.
                 """),
             'button_caption': 'Submit a Job',
             'submit_url': django.core.urlresolvers.reverse(
                 'bulletin:plugins:job-submit')}
        ]
        return context


class ModerationView(braces.views.SetHeadlineMixin,
                     django.views.generic.TemplateView):

    headline = 'Unmoderated Posts'
    template_name = 'plugins/moderation.html'

    def get_context_data(self, **kwargs):
        context = super(ModerationView, self).get_context_data(**kwargs)

        context['unmoderated_posts'] = []

        for plugin in get_active_plugins():

            for unmoderated_post in plugin.model_class().objects.filter(
                    approved=None).order_by('-date_submitted'):
                context['unmoderated_posts'].append(unmoderated_post)

        context['next'] = self.request.GET.get('next', '')

        return context
