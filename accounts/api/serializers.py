from rest_framework import serializers

from accounts.models import UserProfile, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name']


class UserProfileSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField(read_only=True)
    following = serializers.SerializerMethodField()
    class Meta:
        model = UserProfile
        fields = ['url', 'id', 'user', 'name', 'bio', 'birth_date',
                  'profile_img', 'post_count', 'followers', 'following', 'following_count',
                  'followers_count', 'skill', 'created', 'topic', 'timestamp',
                  'verified', 'active']
        depth = 1
        read_only_field = ['id', 'user', 'timestamp',
                           'post_count', 'following_count',
                           'followers_count','verified', 'active']
    
    def get_following(self, obj):
        user = obj.user
        following = user.following.all().values("user")
        return UserSerializer(following,many=True).data
    
    def get_url(self, obj):
        return obj.get_api_url(request=self.context.get('request'))
    
