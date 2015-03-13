from bulletin.api import serializers
from bulletin.tools.plugins.models import Story


class StorySerializer(serializers.PostSerializer):

    submitter = serializers.UserSerializer(many=False, required=False)
    links = serializers.LinkSerializer(many=True, required=False)
    category = serializers.CategorySerializer(many=True, required=False)

    class Meta:
        model = Story
        fields = ('id', 'title', 'url', 'approved', 'pub_date',
                  'submitter', 'position', 'links', 'blurb',
                  'date', 'category')
