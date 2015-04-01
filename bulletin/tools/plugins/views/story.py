from braces.views import SetHeadlineMixin
from django.conf import settings
from django.views.generic import ListView

from bulletin.models import Category
from bulletin.views import PostSubmitView, PostUpdateView, SidebarView
from bulletin.tools.plugins.forms import story as forms
from bulletin.tools.plugins.models import Story


class StorySubmitView(PostSubmitView):

    model = Story
    form_class = forms.StorySubmitForm
    headline = 'Submit a Story'


class StoryUpdateView(PostUpdateView):

    model = Story
    form_class = forms.StoryUpdateForm
    headline = 'Update Story'


class StoryListView(SetHeadlineMixin,
                    ListView,
                    SidebarView):

    model = Story
    template_name = 'plugins/story_list.html'
    paginate_by = settings.NUM_POSTS_ON_FRONT_PAGE
    headline = 'News'

    def get_queryset(self, *args, **kwargs):
        queryset = Story.objects.filter(approved=True).order_by('-pub_date',
                                                                'title')

        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        return queryset

    def get_context_data(self, **kwargs):
        context = super(StoryListView, self).get_context_data(**kwargs)

        context['categories'] = Category.objects.all().order_by('name')

        category_id = self.request.GET.get('category')
        if category_id:
            context['current_filter_name'] = Category.objects.get(
                pk=category_id).name
        else:
            context['current_filter_name'] = 'All'

        return context
