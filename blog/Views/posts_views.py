from rest_framework.views import APIView
from rest_framework import mixins, viewsets
from blog.Serializers.post_serializers import PostsSerializers
from blog.models import Posts
from rest_framework.permissions import IsAuthenticated


class PostsViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.CreateModelMixin,
):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializers
    permission_classes = [IsAuthenticated]
