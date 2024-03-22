from rest_framework import viewsets, mixins
from blog.models import Comment
from blog.Serializers.comments_serializers import CommentSerializers
from rest_framework.permissions import IsAuthenticated



class CommentsViewSet(
    viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin
):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticated]

