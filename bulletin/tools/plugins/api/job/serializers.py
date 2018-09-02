from rest_framework.serializers import SerializerMethodField

from bulletin.api import serializers
from bulletin.tools.plugins.models import Job


class JobSerializer(serializers.PostSerializer):

    post_type = SerializerMethodField(source="get_post_type")
    links = serializers.LinkSerializer(many=True, required=False,
                                       read_only=True)

    class Meta:
        model = Job
        fields = ('id', 'title', 'url', 'approved', 'pub_date',
                  'submitter', 'post_type', 'position', 'links',
                  'organization')

    def get_post_type(self, _):
        return "JOB"
