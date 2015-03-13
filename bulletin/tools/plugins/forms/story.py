from datetimewidget.widgets import DateTimeWidget, DateWidget
import django.forms
from form_utils.widgets import ImageWidget

from ..models import Story


class StorySubmitForm(django.forms.ModelForm):

    class Meta:
        model = Story
        fields = ['title',
                  'url',
                  'blurb',
                  'image',
                  'date',
                  'category']
        labels = {
            'date': 'Publish Date of News'
        }
        widgets = {
            'date': DateWidget(usel10n=True, bootstrap_version=3)
        }


class StoryUpdateForm(django.forms.ModelForm):

    class Meta:
        model = Story
        fields = ['title',
                  'url',
                  'blurb',
                  'image',
                  'date',
                  'category',
                  'approved',
                  'include_in_newsletter',
                  'pub_date']
        labels = {
            'date': 'Publish Date of News'
        }
        widgets = {
            'image': ImageWidget(),
            'date': DateWidget(usel10n=True, bootstrap_version=3),
            'pub_date': DateTimeWidget(usel10n=True, bootstrap_version=3)
        }
