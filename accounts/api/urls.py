from django.urls import path, include

from .views import ProfileListAPIView


urlpatterns = [
    path('list', ProfileListAPIView.as_view(), name='profile_list'),
]