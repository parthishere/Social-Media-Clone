from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response

from accounts.api.serializers import UserProfileSerializer
from accounts.models import UserProfile, User

from post.models import Post
from post.api.serializers import PostSerializer



class ProfileListAPIView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = ['slug',]
    
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)
    
    
@api_view(['GET',])
def user_posts_api_view(request):
    user = request.user
    queryset = Post.objects.filter(user=user)
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data)
    