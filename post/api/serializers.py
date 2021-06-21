from rest_framework import serializers

from post.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        depth = 1
        
    def create(self, validated_data):
        post = super(PostSerializer, self).create(validated_data)
        post.user = self.context.get('request').user
        post.save()
        return post
        