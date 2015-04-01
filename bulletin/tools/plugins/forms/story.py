from datetimewidget.widgets import DateTimeWidget, DateWidget
import django.forms
from form_utils.widgets import ImageWidget

from ....models import Category
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
            'image': 'Image (10Mb limit)',
            'date': 'Date originally published - if unknown, select today.'
        }
        widgets = {
            'date': DateWidget(usel10n=True, bootstrap_version=3)
        }

    def __init__(self, *args, **kwargs):
        super(StorySubmitForm, self).__init__(*args, **kwargs)
        # Don't show categories, only subcategories:
        self.fields['category'].queryset = Category.objects.exclude(
            parent=None).order_by('name')


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

    def __init__(self, *args, **kwargs):
        super(StoryUpdateForm, self).__init__(*args, **kwargs)
        # Don't show categories, only subcategories:
        self.fields['category'].queryset = Category.objects.exclude(
            parent=None).order_by('name')
