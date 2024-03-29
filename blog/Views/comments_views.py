from rest_framework import viewsets, mixins
from blog.models import Comment
from blog.Serializers.comments_serializers import CommentSerializers
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.response import Response


class CommentsViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        instance = serializer.save()
        cache.delete("comments_list_cache_key")

    def list(self, request, *args, **kwargs):
        cache_key = "comments_list_cache_key"
        cached_data = cache.get(cache_key)
        if cached_data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            cache.set(cache_key, serializer.data, timeout=60 * 15)
            return Response(serializer.data)
        return Response(cached_data)
