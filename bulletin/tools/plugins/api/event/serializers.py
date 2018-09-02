from rest_framework.serializers import SerializerMethodField

from bulletin.api import serializers
from bulletin.tools.plugins.models import Event


class EventSerializer(serializers.PostSerializer):

    post_type = SerializerMethodField(source="get_post_type")
    links = serializers.LinkSerializer(many=True, required=False,
                                       read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'title', 'url', 'approved', 'pub_date',
                  'submitter', 'position', 'links', 'post_type',
                  'start_date', 'end_date', 'time', 'organization',
                  'location')

    def get_post_type(self, _):
        return "EVENT"
