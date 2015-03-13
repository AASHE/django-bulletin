from bulletin.api import permissions
from bulletin.api.views import PostList, PostDetail
import serializers
from bulletin.tools.plugins.models import Event


class EventList(PostList):
    queryset = Event.objects.all()
    serializer_class = serializers.EventSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class EventDetail(PostDetail):
    serializer_class = serializers.EventSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)
