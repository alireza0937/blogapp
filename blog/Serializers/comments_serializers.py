from rest_framework import serializers
from blog.models import Comment


class CommentSerializers(serializers.ModelSerializer):

    class Meta:
        model = Comment
        exclude = ["id"]

    def validate_answer(self, value):
        post = self.initial_data.get("post")
        if value.post_id != int(post):
            raise serializers.ValidationError(
                "Parent comment does not belong to the same post."
            )
        return value
