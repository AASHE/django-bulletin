from braces.views import SetHeadlineMixin
from django.conf import settings
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
    headline = 'Update an Event'


class EventListView(SetHeadlineMixin,
                    ListView,
                    SidebarView):

    model = Event
    queryset = Event.objects.filter(approved=True).order_by('-pub_date')
    template_name = 'plugins/event_list.html'
    paginate_by = settings.NUM_POSTS_ON_FRONT_PAGE
    headline = 'Events'

    def get_queryset(self):
        queryset = super(EventListView, self).get_queryset()
        if 'category' in self.request.GET:
            category = Category.objects.get(name=self.request.GET['category'])
            queryset.filter(category_id=category.id)
        return queryset
