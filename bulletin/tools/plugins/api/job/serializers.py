from bulletin.api import serializers
from bulletin.tools.plugins.models import Job


class JobSerializer(serializers.PostSerializer):

    links = serializers.LinkSerializer(many=True, required=False)

    class Meta:
        model = Job
        fields = ('id', 'title', 'url', 'approved', 'pub_date',
                  'submitter', 'position', 'links', 'organization')
