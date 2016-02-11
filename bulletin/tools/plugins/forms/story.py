from datetimewidget.widgets import DateTimeWidget, DateWidget
from django.conf import settings
import django.forms
from form_utils.widgets import ImageWidget

from ....forms import PostUpdateForm, PostSubmitForm
from ....models import Category
from ..models import Story

story_field_labels = {
    'url': 'URL',
    'image': 'Image (Landscape orientation - 10Mb limit) *',
    'date': 'Date originally published - if unknown, select today.',
    'categories': 'Secondary Categories (choose up to 2)'
}

if getattr(settings,
           'MAX_STORY_TITLE_LENGTH',
           False):
    story_field_labels['title'] = 'Title - {0} characters maximum'.format(
        settings.MAX_STORY_TITLE_LENGTH)

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
    'pub_date': DateTimeWidget(usel10n=True, bootstrap_version=3),
    'categories': django.forms.SelectMultiple(
        attrs={'id': 'id_secondary_categories'})
}

if getattr(settings,
           'MAX_STORY_TITLE_LENGTH',
           False):
    story_widgets['title'] = django.forms.Textarea(
        attrs={'maxlength': settings.MAX_STORY_TITLE_LENGTH,
               'rows': 1})

if getattr(settings,
           'MAX_STORY_BLURB_LENGTH',
           False):
    story_widgets['blurb'] = django.forms.Textarea(
        attrs={'maxlength': settings.MAX_STORY_BLURB_LENGTH,
               'rows': 4})


class StorySubmitForm(PostSubmitForm):

    primary_category = django.forms.ModelMultipleChoiceField(
        queryset=Category.objects.exclude(
            parent=None).exclude(private=True).order_by('name'),
        required=False)

    class Meta:
        model = Story
        fields = ['title',
                  'url',
                  'blurb',
                  'image',
                  'date',
                  'primary_category',
                  'categories']
        labels = story_field_labels
        help_texts = story_help_texts
        widgets = story_widgets


class StoryUpdateForm(PostUpdateForm):

    primary_category = django.forms.ModelMultipleChoiceField(
        queryset=Category.objects.exclude(
            parent=None).order_by('name'),
        required=False)

    class Meta:
        model = Story
        fields = ['title',
                  'url',
                  'blurb',
                  'image',
                  'date',
                  'primary_category',
                  'categories',
                  'approved',
                  'include_in_newsletter',
                  'feature',
                  'pub_date']
        labels = story_field_labels
        help_texts = story_help_texts
        widgets = story_widgets

    def __init__(self, *args, **kwargs):
        super(StoryUpdateForm, self).__init__(*args, **kwargs)

        primary_category = self.instance.primary_category

        if primary_category:
            self.fields['primary_category'].initial = [primary_category]
            # Filter primary category from secondary categories list:
            categories_queryset = self.fields['categories'].queryset
            self.fields['categories'].queryset = categories_queryset.exclude(
                pk=primary_category.id)
        else:
            self.fields['primary_category'].initial = None
