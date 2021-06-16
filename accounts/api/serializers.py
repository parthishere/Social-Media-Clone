from rest_framework import serializers

from accounts.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['url', 'id', 'user', 'name', 'bio', 'birth_date',
                  'profile_img', 'post_count', 'followers', 'following', 'following_count',
                  'skill', 'created', 'topic', 'timestamp', 'verified', 'active']
        depth = 1
        read_only_field = ['url', 'id', 'user', 'timestamp',
                           'post_count', 'following_count', 'verified', 'active']
    
    def get_following(self.obj):
        return self.context.get('request').user.following
    
    def get_url(self, obj):
        return obj.get_absolute_uri(self.context.get('request'))
    
