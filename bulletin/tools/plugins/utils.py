from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from bulletin.models import Post


def get_installed_plugins():
    """Yield a list of ContentTypes representing installed plugins.

    Installed plugins are ContentType objects subclassing Post.
    """
    for content_type in ContentType.objects.all():
        model = content_type.model_class()
        if model and issubclass(model, Post) and not model == Post:
            yield content_type


def get_active_plugins():
    """Yield a list of ContentTypes representing plugins that
    are installed and listed in settings.BULLETIN_CONTENT_TYPE_PLUGINS.
    """
    installed_plugins = get_installed_plugins()

    for plugin in installed_plugins:

        if (plugin.app_label == 'plugins' and
            plugin.name in settings.BULLETIN_CONTENT_TYPE_PLUGINS):

            yield plugin


def get_active_plugins_choices():
    """Yield a list of 2-tuples, suitable for the `choices`
    attribute on a ChoiceField.
    """
    active_plugins = get_active_plugins()
    for plugin in active_plugins:
        yield (plugin.model, plugin.name)
