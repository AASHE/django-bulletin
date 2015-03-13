from datetimewidget.widgets import DateTimeWidget, DateWidget
import django.forms

from ..models import Opportunity


class OpportunitySubmitForm(django.forms.ModelForm):

    class Meta:
        model = Opportunity
        fields = ['title',
                  'url',
                  'blurb']


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
