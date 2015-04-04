from braces.views import SetHeadlineMixin
from django.conf import settings
from django.contrib import messages
from django.views.generic import ListView

from bulletin.models import Category
from bulletin.views import PostSubmitView, PostUpdateView, SidebarView
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


class EventListView(SetHeadlineMixin,
                    ListView,
                    SidebarView):

    model = Event
    template_name = 'plugins/event_list.html'
    paginate_by = settings.NUM_POSTS_ON_FRONT_PAGE
    headline = 'Events'

    def get_queryset(self):
        queryset = Event.objects.filter(approved=True).order_by('-pub_date',
                                                                'title')
        if 'category' in self.request.GET:
            category = Category.objects.get(name=self.request.GET['category'])
            queryset.filter(category_id=category.id)
        return queryset
