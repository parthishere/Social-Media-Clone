from rest_framework.views import APIView
from rest_framework import generics
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

from comments.models import Comment
from post.models import Post


def AddComment(APIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def post(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        if serializer.is_valid():
            pass
        