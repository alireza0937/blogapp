from rest_framework import mixins, viewsets
from blog.Serializers.post_serializers import PostsSerializers
from blog.models import Posts
from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from rest_framework.response import Response


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

    @staticmethod
    def _get_all_posts_cache_key():
        return "posts_list_cache_key"

    @staticmethod
    def _get_single_post_cache_key(pk):
        return f"posts_detail_cache_key_{pk}"

    def list(self, request, *args, **kwargs):
        cache_key = self._get_all_posts_cache_key()
        cached_data = cache.get(cache_key)
        if cached_data is None:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            cache.set(cache_key, serializer.data, timeout=60 * 15)
            return Response(serializer.data)
        return Response(cached_data)

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs.get("pk")
        cache_key = self._get_single_post_cache_key(pk)
        cached_data = cache.get(cache_key)
        if cached_data is None:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            cache.set(cache_key, serializer.data, timeout=60 * 15)
            return Response(serializer.data)
        return Response(cached_data)

    def perform_update(self, serializer):
        instance = serializer.save()
        cache.delete(self._get_all_posts_cache_key())
        cache.delete(self._get_single_post_cache_key(instance.pk))

    def perform_create(self, serializer):
        serializer.save()
        cache.delete(self._get_all_posts_cache_key())
