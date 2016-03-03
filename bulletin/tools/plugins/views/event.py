from django.contrib import messages

from bulletin.views import (PostListView,
                            PostSubmitView,
                            PostUpdateView)
from bulletin.tools.plugins.forms import event as forms
from bulletin.tools.plugins.models import Event


class EventSubmitView(PostSubmitView):

    model = Event
    form_class = forms.EventSubmitForm
    headline = 'Submit an Event'


class EventUpdateView(PostUpdateView):

    model = Event
    form_class = forms.EventUpdateForm
    headline = 'Update Event'

    def form_valid(self, form):
        messages.success(self.request, "Event saved.")
        return super(EventUpdateView, self).form_valid(form)


class EventListView(PostListView):

    model = Event
    template_name = 'plugins/event_list.html'
    headline = 'Events'

    def get_queryset(self, *args, **kwargs):
        return super(EventListView, self).get_queryset(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(EventListView, self).get_context_data(**kwargs)
