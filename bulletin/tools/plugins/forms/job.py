from datetimewidget.widgets import DateTimeWidget
from django.forms import ModelForm
from form_utils.widgets import ImageWidget

from ..models import Job


class JobSubmitForm(ModelForm):

    class Meta:
        model = Job
        fields = ['title',
                  'url',
                  'organization',
                  'image']


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
