from braces.views import SetHeadlineMixin
from django.conf import settings
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from bulletin.models import Category
from bulletin.views import PostSubmitView, PostUpdateView, SidebarView
from bulletin.tools.plugins.forms import new_resource as forms
from bulletin.tools.plugins.models import NewResource


class NewResourceSubmitView(PostSubmitView):

    model = NewResource
    form_class = forms.NewResourceSubmitForm
    headline = 'Submit a New Resource'


class NewResourceUpdateView(PostUpdateView):

    model = NewResource
    form_class = forms.NewResourceUpdateForm
    headline = 'Update New Resource'

    def form_valid(self, form):
        messages.success(self.request, "New Resource saved.")
        return super(NewResourceUpdateView, self).form_valid(form)


class NewResourceListView(SetHeadlineMixin,
                          ListView,
                          SidebarView):

    model = NewResource
    template_name = 'plugins/new_resource_list.html'
    paginate_by = settings.NUM_POSTS_ON_FRONT_PAGE
    headline = 'New Resources'

    def get_queryset(self):
        queryset = NewResource.objects.filter(approved=True).order_by(
            '-pub_date',
            'title')
        if 'category' in self.request.GET:
            category = get_object_or_404(Category,
                                         pk=self.request.GET['category'])
            queryset.filter(category_id=category.id)
        return queryset
