from rest_framework import serializers

from accounts.models import UserProfile

class UserProfileSerializer(serializers.Serializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        
    