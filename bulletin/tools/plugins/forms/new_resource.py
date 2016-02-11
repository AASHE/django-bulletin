from datetimewidget.widgets import DateTimeWidget, DateWidget
from django.conf import settings
import django.forms

from ....forms import PostSubmitForm, PostUpdateForm
from ..models import NewResource


new_resource_field_labels = {'url': 'URL'}

if getattr(settings,
           'MAX_NEW_RESOURCE_BLURB_LENGTH',
           False):
    new_resource_field_labels['blurb'] = (
        'Blurb - {0} characters maximum'.format(
            settings.MAX_NEW_RESOURCE_BLURB_LENGTH))

new_resource_widgets = {
    'date': DateWidget(usel10n=True, bootstrap_version=3)
}

if getattr(settings,
           'MAX_NEW_RESOURCE_BLURB_LENGTH',
           False):
    new_resource_widgets['blurb'] = django.forms.Textarea(
        attrs={'maxlength': settings.MAX_NEW_RESOURCE_BLURB_LENGTH,
               'rows': 4})

new_resource_help_texts = {
    'url': 'Provide a full url, e.g., "http://www.example.com/page.html"'
}


class NewResourceSubmitForm(PostSubmitForm):

    class Meta:
        model = NewResource
        fields = ['title',
                  'url',
                  'blurb',
                  'categories']
        widgets = new_resource_widgets
        labels = new_resource_field_labels
        help_texts = new_resource_help_texts


class NewResourceUpdateForm(PostUpdateForm):

    class Meta:
        model = NewResource
        fields = ['title',
                  'url',
                  'blurb',
                  'categories',
                  'approved',
                  'include_in_newsletter',
                  'pub_date']
        widgets = {
            'date': DateWidget(usel10n=True, bootstrap_version=3),
            'pub_date': DateTimeWidget(usel10n=True, bootstrap_version=3)
        }
        labels = new_resource_field_labels
        help_texts = new_resource_help_texts
