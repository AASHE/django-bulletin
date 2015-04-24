from datetimewidget.widgets import DateTimeWidget
import django.forms

from ..models import Opportunity

opportunity_field_labels = {
    'url': 'URL'
}

opportunity_help_texts = {
    'url': 'Provide a full url, e.g., "http://www.example.com/page.html"'
}


class OpportunitySubmitForm(django.forms.ModelForm):

    class Meta:
        model = Opportunity
        fields = ['title',
                  'url',
                  'blurb']
        labels = opportunity_field_labels
        help_texts = opportunity_help_texts


class OpportunityUpdateForm(django.forms.ModelForm):

    class Meta:
        model = Opportunity
        fields = ['title',
                  'url',
                  'blurb',
                  'approved',
                  'include_in_newsletter',
                  'pub_date']
        widgets = {
            'pub_date': DateTimeWidget(usel10n=True, bootstrap_version=3)
        }
        labels = opportunity_field_labels
        help_texts = opportunity_help_texts
