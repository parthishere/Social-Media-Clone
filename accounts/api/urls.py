from django.urls import path, include

from .views import ProfileListAPIView

app_name = 'account-api'

urlpatterns = [
    path('', ProfileListAPIView.as_view(), name='profile_list'),
    path('<int:id>/', ProfileListAPIView.as_view(), name='profile_list'),
    path('follow/<int:id>/', ProfileListAPIView.as_view(), name='profile_list'),
    path('update-profile/', ProfileListAPIView.as_view(), name='profile_list'),
    path('delete-profile/', ProfileListAPIView.as_view(), name='profile_list'),
    # path('/', ProfileListAPIView.as_view(), name='profile_list'),
    # path('list/', ProfileListAPIView.as_view(), name='profile_list'),
]