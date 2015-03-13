from braces.views import SetHeadlineMixin
from django.conf import settings
from django.views.generic import ListView

from bulletin.models import Category
from bulletin.views import PostSubmitView, PostUpdateView, SidebarView
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


class JobListView(SetHeadlineMixin,
                  ListView,
                  SidebarView):

    model = Job
    queryset = Job.objects.filter(approved=True).order_by('-pub_date')
    template_name = 'plugins/job_list.html'
    paginate_by = settings.NUM_POSTS_ON_FRONT_PAGE
    headline = 'Jobs'

    def get_queryset(self):
        queryset = super(JobListView, self).get_queryset()
        if 'category' in self.request.GET:
            category = Category.objects.get(name=self.request.GET['category'])
            queryset.filter(category_id=category.id)
        return queryset
