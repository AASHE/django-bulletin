from rest_framework.serializers import SerializerMethodField

from bulletin.api import serializers
from bulletin.tools.plugins.models import NewResource


class NewResourceSerializer(serializers.PostSerializer):

    post_type = SerializerMethodField(source="get_post_type")
    submitter = serializers.UserSerializer(many=False, required=False,
                                           read_only=True)
    links = serializers.LinkSerializer(many=True, required=False,
                                       read_only=True)
    category = serializers.CategorySerializer(many=True, required=False,
                                              read_only=True)

    class Meta:
        model = NewResource
        fields = ('id', 'title', 'url', 'approved', 'pub_date',
                  'submitter', 'post_type', 'position', 'links',
                  'blurb', 'category')

    def get_post_type(self, _):
        return "NEWRESOURCE"
