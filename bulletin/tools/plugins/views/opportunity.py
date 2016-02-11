from django.contrib import messages

from bulletin.views import (PostListView,
                            PostSubmitView,
                            PostUpdateView)
from bulletin.tools.plugins.forms import opportunity as forms
from bulletin.tools.plugins.models import Opportunity


class OpportunitySubmitView(PostSubmitView):

    model = Opportunity
    form_class = forms.OpportunitySubmitForm
    headline = 'Submit an Opportunity'


class OpportunityUpdateView(PostUpdateView):

    model = Opportunity
    form_class = forms.OpportunityUpdateForm
    headline = 'Update Opportunity'

    def form_valid(self, form):
        messages.success(self.request, "Opportunity saved.")
        return super(OpportunityUpdateView, self).form_valid(form)


class OpportunityListView(PostListView):

    model = Opportunity
    template_name = 'plugins/opportunity_list.html'
    headline = 'Opportunities'

    def get_queryset(self, *args, **kwargs):
        return super(OpportunityListView, self).get_queryset(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(OpportunityListView, self).get_context_data(**kwargs)
