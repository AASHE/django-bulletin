from datetimewidget.widgets import DateTimeWidget, DateWidget
from django.forms import ModelForm

from ..models import Event

event_field_labels = {
    'title': 'Title of Event',
    'url': 'URL of Event',
    'start_date': 'Start Date of Event',
    'end_date': 'End Date of Event (if different from Start Date)',
    'time': 'Time of Event',
    'organization': 'Organization Hosting Event',
    'location': 'Location of Event'
}

event_help_texts = {
    'url': 'Provide a full url, e.g., "http://www.example.com/page.html"',
    'time': 'E.g., "2:00 p.m. Eastern"',
    'location': ('If an online event, please enter "Online". If at a '
                 'geographical location, please enter the City, State, '
                 'e.g., "Baltimore, Maryland"')
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
        help_texts = event_help_texts


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
        help_texts = event_help_texts
