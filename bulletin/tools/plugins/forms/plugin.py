import django.forms

from ..utils import get_active_plugins_choices


class ChoosePostTypeForm(django.forms.Form):

    post_types = django.forms.ChoiceField(
        choices=get_active_plugins_choices())

    class Meta:
        fields = ['post_types']
