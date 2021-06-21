from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
    IsAdminUser
)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from comments.api.serializers import CommentSerializer
from post.api.serializers import PostSerializer
from accounts.api.serializers import UserProfileSerializer, UserSerilizer

from django.shortcuts import get_object_or_404
from comments.models import Comment
from post.models import Post
from .permissions import IsOwnerOrReadOnly


class AddComment(APIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            if self.request.data.get('parent'):
                serializer.save(user=self.request.user, parent=self.request.data.get('parent'))
            else:
                serializer.save(user=self.request.user)
            return Response(serializer.data)
      
 
@api_view(['GET'])   
@permission_classes([AllowAny])  
def comment_list_on_post(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    serializer1 = PostSerializer(post, many=False)
    
    comments = post.comment_post.all()
    serializer2 = CommentSerializer(comments, many=True)
    
    # Serializer_list = [serializer1.data, serializer2.data]

    # content = {
    #     'status': 1, 
    #     'responseCode' : status.HTTP_200_OK, 
    #     'data': Serializer_list,

    #     }
    return Response(serializer2.data)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def all_comment_list(request):
    serializer = CommentSerializer(Comment.objects.all(), many=True)
    return Response(serializer.data)


class UpdateComment(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = CommentSerializer
    lookup_field = ['pk']
    
    def patch(self, *args, **kwargs):
        data = self.request.data
        comment = get_object_or_404(Comment,pk=self.lookup_field)
        serializer = self.serializer_class(comment,data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
  
      
class DeleteComment(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = ['pk']
    
