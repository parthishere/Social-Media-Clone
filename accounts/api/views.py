from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from accounts.api.serializers import UserProfileSerializer
from accounts.models import UserProfile, User

from post.models import Post
from post.api.serializers import PostSerializer



class ProfileListAPIView(generics.ListCreateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]
    lookup_field = ['slug',]
    
    def list(self, request):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = self.get_queryset()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)
    
@api_view(['GET',])
@permission_classes([IsAuthenticated])    
def get_self_profile(request):
    

@api_view(['GET',])
def user_posts_api_view(request):
    user = request.user
    queryset = Post.objects.filter(user=user)
    serializer = PostSerializer(queryset, many=True)
    return Response(serializer.data)

def get_self_profile(request) :
    user = request.user.user_profile