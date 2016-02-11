from datetimewidget.widgets import DateTimeWidget
from form_utils.widgets import ImageWidget

from ....forms import PostSubmitForm, PostUpdateForm
from ..models import Job

job_field_labels = {
    'image': 'Institution Logo (10Mb Limit)',
    'url': 'URL',
    'categories': 'Categories (choose up to 3)'
}

job_help_texts = {
    'url': 'Provide a full URL, e.g., "http://www.example.com/page.html"'
}

field_widgets = {
    'image': ImageWidget(attrs={'required': 'required'})
}


class JobSubmitForm(PostSubmitForm):

    class Meta:
        model = Job
        fields = ['title',
                  'url',
                  'organization',
                  'image',
                  'categories']
        labels = job_field_labels
        help_texts = job_help_texts
        widgets = field_widgets


class JobUpdateForm(PostUpdateForm):

    class Meta:
        model = Job
        fields = ['title',
                  'url',
                  'organization',
                  'image',
                  'categories',
                  'approved',
                  'include_in_newsletter',
                  'pub_date']
        widgets = {
            'pub_date': DateTimeWidget(usel10n=True, bootstrap_version=3),
            'image': ImageWidget(),
        }
        labels = job_field_labels
        help_texts = job_help_texts
