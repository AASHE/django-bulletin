from datetimewidget.widgets import DateTimeWidget
from django.conf import settings
import django.forms

from ....forms import PostSubmitForm, PostUpdateForm
from ..models import Opportunity

opportunity_field_labels = {
    'url': 'URL',
    'categories': 'Categories (choose up to 3)'
}

if getattr(settings,
           'MAX_OPPORTUNITY_BLURB_LENGTH',
           False):
    opportunity_field_labels['blurb'] = (
        'Blurb - {0} characters maximum'.format(
            settings.MAX_OPPORTUNITY_BLURB_LENGTH))

opportunity_help_texts = {
    'url': 'Provide a full url, e.g., "http://www.example.com/page.html"'
}

opportunity_widgets = {
    'pub_date': DateTimeWidget(usel10n=True, bootstrap_version=3)
}

if getattr(settings,
           'MAX_OPPORTUNITY_BLURB_LENGTH',
           False):
    opportunity_widgets['blurb'] = django.forms.Textarea(
        attrs={'maxlength': settings.MAX_OPPORTUNITY_BLURB_LENGTH,
               'rows': 4})


class OpportunitySubmitForm(PostSubmitForm):

    class Meta:
        model = Opportunity
        fields = ['title',
                  'url',
                  'blurb',
                  'categories']
        widgets = opportunity_widgets
        labels = opportunity_field_labels
        help_texts = opportunity_help_texts


class OpportunityUpdateForm(PostUpdateForm):

    class Meta:
        model = Opportunity
        fields = ['title',
                  'url',
                  'blurb',
                  'categories',
                  'approved',
                  'include_in_newsletter',
                  'pub_date']
        widgets = opportunity_widgets
        labels = opportunity_field_labels
        help_texts = opportunity_help_texts
