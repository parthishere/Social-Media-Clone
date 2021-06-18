from rest_framework import Response 
from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView

from accounts.api.serializers import UserSerilizer, UserProfileSerializer
from post.api.serializers import PostSerializer

from accounts.models import UserProfile, User
from post.models import Post


def feed(request):
   pass 

def following_user_post(request):
    pass

def top_posts(request):
    pass

