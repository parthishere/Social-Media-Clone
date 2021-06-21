from rest_framework import serializers

from comments.models import Comment
from post.api.serializers import PostSerializer

class CommentSerializer(serializers.ModelSerializer):
    post = PostSerializer(many=False, read_only=True)
    class Meta:
        model = Comment
        fields = '__all__'
        depth = 1