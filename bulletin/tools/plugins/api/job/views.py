from bulletin.api import permissions
from bulletin.api.views import PostList, PostDetail
import serializers
from bulletin.tools.plugins.models import Job


class JobList(PostList):
    queryset = Job.objects.all()
    serializer_class = serializers.JobSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)


class JobDetail(PostDetail):
    serializer_class = serializers.JobSerializer
    permission_classes = (permissions.IsAdminUserOrReadOnly,)
