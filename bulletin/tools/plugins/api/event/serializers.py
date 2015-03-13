from bulletin.api import serializers
from bulletin.tools.plugins.models import Event


class EventSerializer(serializers.PostSerializer):

    links = serializers.LinkSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'title', 'url', 'approved', 'pub_date',
                  'submitter', 'position', 'links',
                  'start_date', 'end_date', 'time', 'organization',
                  'location')
