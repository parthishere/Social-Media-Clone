from rest_framework import generics
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from .serializers import UserProfileSerializer
from accounts.models import UserProfile, User



class ProfileListAPIView(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    