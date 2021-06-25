from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.response import Response

from rest_framework import filters

from .serializers import NotificationSerializer
from notifications.models import Notification
from accounts.models import User, UserProfile
from accounts.api.serializers import  UserProfileSerializer

from post.models import Post
from post.api.serializers import PostSerializer

from comments.models import Comment
from comments.api.serializers import CommentSerializer
# Create your views here.

class NotificationListAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    permission_classes = [IsAdminUser,]
    serializer_class = NotificationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['to_user__username', 'from_user__username', 'content', 'notification_type', ]
    ordering_fields = '__all__'
    
class UserNotificationListAPIView(generics.ListAPIView):
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticated,]
    serializer_class = NotificationSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['to_user__username', 'from_user__username', 'content', 'notification_type', ]
    ordering_fields = '__all__'
    
    def get_queryset(self):
        return Notification.objects.filter(to_user__in=self.request.user)
    
    
def read_notification(request):
    pass

def delete_notification(request):
    pass

    
        