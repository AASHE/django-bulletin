from django.contrib import messages

from bulletin.views import (PostListView,
                            PostSubmitView,
                            PostUpdateView)
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

    def form_valid(self, form):
        messages.success(self.request, "Story saved.")
        return super(StoryUpdateView, self).form_valid(form)


class StoryListView(PostListView):

    model = Story
    template_name = 'plugins/story_list.html'
    headline = 'News'

    def get_queryset(self, *args, **kwargs):
        return super(StoryListView, self).get_queryset(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(StoryListView, self).get_context_data(**kwargs)
