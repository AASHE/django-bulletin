from bulletin.api import permissions
from bulletin.api.views import PostList, PostDetail
import serializers
from bulletin.tools.plugins.models import NewResource


class NewResourceList(PostList):
    queryset = NewResource.objects.all()
    serializer_class = serializers.NewResourceSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class NewResourceDetail(PostDetail):
    serializer_class = serializers.NewResourceSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)
