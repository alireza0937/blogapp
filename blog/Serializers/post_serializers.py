from rest_framework import serializers
from blog.models import Posts


class PostsSerializers(serializers.ModelSerializer):

    class Meta:
        model = Posts
        fields = "__all__"
