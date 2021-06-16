from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404

from rest_framework import filters
from accounts.api.serializers import UserProfileSerializer
from accounts.models import UserProfile, User

from .permissions import IsOwnerOrReadOnly
from post.models import Post
from post.api.serializers import PostSerializer

        
@api_view(['GET',])
@permission_classes([IsOwnerOrReadOnly,])    
def get_self_profile(request):
    user = request.user.user_profile
    serializer = UserProfileSerializer(user, many=False)
    return Response(serializer.data)
    
    
class UpdateSelfProfile(APIView):
    queryset = UserProfile.objects.all(active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    
    def patch(self, *args, **kwargs):
        user_profile = self.request.user.user_profile
        serializer = self.serializer_class(user_profile, data=self.request.data, partial=True)
        if serializer.is_valid:
            user = serializer.save().user
            response = {'success': True, 'message': 'successfully updated your info',
                        'user': UserProfileSerializer(user).data}
            
            new_email = self.request.data.get('email')
            user = self.request.user
            if new_email is not None:
                user.email = new_email
                user_profile.email_verified = False
                user.save()
                user_profile.save()
            return Response(response, status=200)
        
        else:
            response = serializer.errors
            return Response(response, status=401)
        
class ImageUpdateAPIView(APIView):
    queryset = UserProfile.objects.all(active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    
    def patch(self, *args, **kwargs):
        pass
 
 
 
@api_view(['POST',])
@permission_classes([IsOwnerOrReadOnly,])      
def delete_self_profile_img(request):
    user_profile = request.user.user_profile
    user = request.user
    try:
        user_profile.profile_pic = 'default.png'
        user_profile.save()
    
        response = { 'deleted': True, }
        return Response(response ,status=status.HTTP_200_OK)
    except:
        response = { 'deleted': False, }
        return Response(response ,status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET',])
@permission_classes([IsOwnerOrReadOnly,]) 
def get_self_followers(request):
    user_profile = request.user.user_profile
    followers = user_profile.followers
    serializer = UserProfileSerializer(followers, many=True)
    return Response(serializer.data)


@api_view(['GET',])
@permission_classes([IsOwnerOrReadOnly,])    
def get_self_following(request):
    user_profile = request.user.user_profile
    following_users = request.user.following
    serializer = UserProfileSerializer(following_users, many=True)
    
    return Response(serializer.data)

@api_view(['GET',])
@permission_classes([AllowAny])
def retrive_profile(request, id):
    user_profile = get_object_or_404(UserProfile)
    serializer = UserProfileSerializer(user_profile, many=False)
    return Response(serializer.data)

class UserProfileListAPI(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = [UserProfileSerializer]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__first_name', 'bio', 'name', 'following__user__username__in']
    ordering_fields = '__all__'
    
    def get_serializer_context(self, *args, **kwargs):
        return { "request":self.request }
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_requested_user(request, id):
    """ Here *id* is requested user's *id* """
    self_profile = request.user.user_profile
    requested_user, user, added = self_profile.add_or_remove_to_following(id=id)
    
    serializer = UserProfileSerializer(self_profile, many=False)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([AllowAny])


# @api_view(['GET',])
# def user_posts_api_view(request):
#     user = request.user
#     queryset = Post.objects.filter(user=user)
#     serializer = PostSerializer(queryset, many=True)
#     return Response(serializer.data)

# def get_self_profile(request) :
#     user = request.user.user_profile