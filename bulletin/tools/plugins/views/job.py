from django.contrib import messages

from bulletin.views import (PostListView,
                            PostSubmitView,
                            PostUpdateView)
from bulletin.tools.plugins.forms import job as forms
from bulletin.tools.plugins.models import Job


class JobSubmitView(PostSubmitView):

    model = Job
    form_class = forms.JobSubmitForm
    headline = 'Submit a Job'


class JobUpdateView(PostUpdateView):

    model = Job
    form_class = forms.JobUpdateForm
    headline = 'Update Job'

    def form_valid(self, form):
        messages.success(self.request, "Job saved.")
        return super(JobUpdateView, self).form_valid(form)


class JobListView(PostListView):

    model = Job
    template_name = 'plugins/job_list.html'
    headline = 'Jobs'

    def get_queryset(self, *args, **kwargs):
        return super(JobListView, self).get_queryset(*args, **kwargs)

    def get_context_data(self, **kwargs):
        return super(JobListView, self).get_context_data(**kwargs)
