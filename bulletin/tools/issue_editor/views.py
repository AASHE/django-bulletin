from braces.views import (SetHeadlineMixin,
                          StaffuserRequiredMixin)
from django.views.generic import ListView

from bulletin.models import Issue, Newsletter


class NewsletterIssueListView(StaffuserRequiredMixin,
                              SetHeadlineMixin,
                              ListView):

    model = Issue
    template_name = 'issue_editor/newsletter_issue_list.html'
    headline = 'issues'
    paginate_by = 5

    def get_newsletter(self):
        return Newsletter.objects.get(pk=self.kwargs['pk'])

    def get_queryset(self):
        newsletter = Newsletter.objects.get(pk=self.kwargs['pk'])
        return Issue.objects.filter(newsletter=newsletter)

    def get_context_data(self, **kwargs):
        context = super(NewsletterIssueListView, self).get_context_data(
            **kwargs)
        context['newsletter'] = self.get_newsletter()
        return context
