from datetimewidget.widgets import DateTimeWidget, DateWidget
import django.forms

from ..models import NewResource


class NewResourceSubmitForm(django.forms.ModelForm):

    class Meta:
        model = NewResource
        fields = ['title',
                  'url',
                  'blurb']
        widgets = {
            'date': DateWidget(usel10n=True, bootstrap_version=3)
        }


class NewResourceUpdateForm(django.forms.ModelForm):

    class Meta:
        model = NewResource
        fields = ['title',
                  'url',
                  'blurb',
                  'approved',
                  'include_in_newsletter',
                  'pub_date']
        widgets = {
            'date': DateWidget(usel10n=True, bootstrap_version=3),
            'pub_date': DateTimeWidget(usel10n=True, bootstrap_version=3)
        }
