from datetimewidget.widgets import DateTimeWidget
from django.forms import ModelForm
from form_utils.widgets import ImageWidget

from ..models import Job

job_field_labels = {
    'image': 'Image (10Mb Limit)',
    'url': 'URL'
}

job_help_texts = {
    'url': 'Provide a full url, e.g., "http://www.example.com/page.html"'
}

field_widgets = {
    'image': ImageWidget(attrs={'required': 'required'})
}


class JobSubmitForm(ModelForm):

    class Meta:
        model = Job
        fields = ['title',
                  'url',
                  'organization',
                  'image']
        labels = job_field_labels
        help_texts = job_help_texts
        widgets = field_widgets


class JobUpdateForm(ModelForm):

    class Meta:
        model = Job
        fields = ['title',
                  'url',
                  'organization',
                  'image',
                  'approved',
                  'include_in_newsletter',
                  'pub_date']
        widgets = {
            'pub_date': DateTimeWidget(usel10n=True, bootstrap_version=3),
            'image': ImageWidget(),
        }
        labels = job_field_labels
        help_texts = job_help_texts
