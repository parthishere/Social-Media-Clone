from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

from .serializers import NotificationSerializer
from notifications.models import Notification
from accounts.models import User, UserProfile
from accounts.api.serializers import  UserProfileSerializer

from post.models import Post
from post.api.serializers import PostSerializer

from comments.models import Comment
from comments.api.serializers import CommentSerializer
# Create your views here.

class NotificationListAPIView(APIView):
    queryset = Notification.objects.all()
    permission_classes = [IsAdminUser,]
    serializer_class = NotificationSerializer
    
    def get(self, *args, **kwargs):
        pass