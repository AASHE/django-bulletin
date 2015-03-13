from bulletin.api import permissions
from bulletin.api.views import PostList, PostDetail
import serializers
from bulletin.tools.plugins.models import Story


class StoryList(PostList):
    queryset = Story.objects.all()
    serializer_class = serializers.StorySerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class StoryDetail(PostDetail):
    serializer_class = serializers.StorySerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)
