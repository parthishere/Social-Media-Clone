from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.exceptions import ValidationError

from accounts.api.serializers import UserProfileSerializer
from accounts.models import UserProfile, User

from post.models import Post
from post.api.serializers import PostSerializer
from .permissions import IsOwnerOrReadOnly



class PostListAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    
    def get_queryset(self):
        user = self.request.user
        return Post.objects.filter(user=user)
    

        
    
    
    
# class UserPostListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = PostSerializer
#     permission_classes = [permissions.IsAdminUser]
    
#     def list(self, request):
#         queryset = Post.objects.filter(user=request.user)
#         PostSerializer(queryset, many=True)
#         return Response(PostSerializer.data)
    
#     def perform_create(self, serializer):
#         queryset = PostSerializer.objects.filter(title=serializer.validate_data.get('title'))
#         if queryset.exists():
#             raise ValidationError('Title must be unique')
#         serializer.save(user=self.request.user) 
