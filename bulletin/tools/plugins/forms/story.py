from datetimewidget.widgets import DateTimeWidget, DateWidget
from django.conf import settings
import django.forms
from form_utils.widgets import ImageWidget

from ....models import Category
from ..models import Story

story_field_labels = {
    'url': 'URL',
    'image': 'Image (10Mb limit)',
    'date': 'Date originally published - if unknown, select today.'
}
if getattr(settings,
           'MAX_STORY_BLURB_LENGTH',
           False):
    story_field_labels['blurb'] = 'Blurb - {0} characters maximum'.format(
        settings.MAX_STORY_BLURB_LENGTH)

story_help_texts = {
    'url': 'Provide a full url, e.g., "http://www.example.com/page.html"'
}

story_widgets = {
    'image': ImageWidget(),
    'date': DateWidget(usel10n=True, bootstrap_version=3),
    'pub_date': DateTimeWidget(usel10n=True, bootstrap_version=3)
}
if getattr(settings,
           'MAX_STORY_BLURB_LENGTH',
           False):
    story_widgets['blurb'] = django.forms.Textarea(
        attrs={'maxlength': settings.MAX_STORY_BLURB_LENGTH,
               'rows': 4})


class StorySubmitForm(django.forms.ModelForm):

    class Meta:
        model = Story
        fields = ['title',
                  'url',
                  'blurb',
                  'image',
                  'date',
                  'category']
        labels = story_field_labels
        help_texts = story_help_texts
        widgets = story_widgets

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
                  'feature',
                  'pub_date']
        labels = story_field_labels
        help_texts = story_help_texts
        widgets = story_widgets

    def __init__(self, *args, **kwargs):
        super(StoryUpdateForm, self).__init__(*args, **kwargs)
        # Don't show categories, only subcategories:
        self.fields['category'].queryset = Category.objects.exclude(
            parent=None).order_by('name')
