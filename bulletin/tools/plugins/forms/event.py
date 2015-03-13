from datetimewidget.widgets import DateTimeWidget, DateWidget
from django.forms import ModelForm

from ..models import Event

event_field_labels = {
    'title': 'Title of Event',
    'url': 'URL of Event',
    'start_date': 'Start Date of Event',
    'end_date': 'End Date of Event',
    'time': 'Time of Event',
    'organization': 'Organization Hosting Event',
    'location': 'Location of Event'
}


class EventSubmitForm(ModelForm):

    class Meta:
        model = Event
        fields = ['title',
                  'url',
                  'start_date',
                  'end_date',
                  'time',
                  'organization',
                  'location']
        labels = event_field_labels
        widgets = {
            'start_date': DateWidget(usel10n=True, bootstrap_version=3),
            'end_date': DateWidget(usel10n=True, bootstrap_version=3)
        }


class EventUpdateForm(ModelForm):

    class Meta:
        model = Event
        fields = ['title',
                  'url',
                  'start_date',
                  'end_date',
                  'time',
                  'organization',
                  'location',
                  'approved',
                  'include_in_newsletter',
                  'pub_date']
        labels = event_field_labels
        widgets = {
            'start_date': DateWidget(usel10n=True, bootstrap_version=3),
            'end_date': DateWidget(usel10n=True, bootstrap_version=3),
            'pub_date': DateTimeWidget(usel10n=True, bootstrap_version=3)
        }
