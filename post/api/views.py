from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from rest_framework import filters
from rest_framework import parsers

from accounts.api.serializers import UserProfileSerializer
from accounts.models import UserProfile, User

from post.models import Post
from post.api.serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly

from accounts.api.serializers import UserSerilizer



class PostListAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ['user__username', 'user__first_name', 'timestamp']
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    ordering_fields = '__all__'
    
    
    
class PostCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    parser_classes = [parsers.FileUploadParser]
    
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return Response(serializer.data)
    
    def get_serializer_context(self, *args, **kwargs):
        return { 'request': self.request }
    
    
class UpdatePost(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = [parsers.FileUploadParser]
    lookup_field = ['pk']
    
  
class DeletePost(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = ['pk']
    
    
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def like_unlike_post(request, pk=None):
    user = request.user
    try:
        post = get_object_or_404(Post, pk=pk)
    except:
        print("Cant Find Post!")
    if user in post.likes.all():
        post.likes.remove(user)
        return Response({'detail': 'User Removed from like'})
    else:
        post.likes.add(user)
        return Response({'detail': 'User Added to like'})
 

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])  
def see_all_liked_user(request, pk=None):
    user = request.user
    
    post = get_object_or_404(Post, pk=pk)
    qs = post.likes.all()
    if user in qs:
        qs.pop(user=user)
        
    return UserSerilizer(qs, many=True).data


@api_view(['GET'])
@permission_classes([IsOwnerOrReadOnly])  
def self_posts(request):
    user = request.user
    posts = user.post_user
    return Response(PostSerializer(posts, many=True).data)


def see_following_users_post(request, id=None): # feed
    pass


@api_view(['GET'])
def user_posts(request, username=None):
    user_profile = UserProfile.objects.get(username=username) 
    posts = None
    if request.user.is_authenticated:
        if (request.user == user_profile.user) or (request.user in user_profile.followers.all()):
            posts = user_profile.user.post_user or None
        else:
            None
    else:
        pass
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def save_post(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    data = {}
    user_profile = request.user.user_profile
    if post in user_profile.saved_posts.all():
        user_profile.saved_posts.remove(post)
        data['data'] = 'post removed from saved'
    else:
        user_profile.saved_posts.add(post)
        data['data'] = 'post added to saved'
        
    user_profile.save()
    
    return Response(data)

class SavedPostListAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]    
    
    def list(self, request, *args, **kwargs):
        user = request.user
        user_profile = user.user_profile
        saved_post = user_profile.saved_post.all()
        return saved_post
