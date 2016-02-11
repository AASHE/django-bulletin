from django.contrib import messages

from bulletin.views import (PostListView,
                            PostSubmitView,
                            PostUpdateView)
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


class NewResourceListView(PostListView):

    model = NewResource
    template_name = 'plugins/new_resource_list.html'
    headline = 'New Resources'

    def get_queryset(self, *args, **kwargs):
        return super(NewResourceListView, self).get_queryset(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(NewResourceListView, self).get_context_data(**kwargs)
