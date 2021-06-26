from django.urls import path

from .views import (
    NotificationListAPIView,
    UserAllNotificationListAPIView,
    UserUnreadNotificationListAPIView,
    read_notification,
    delete_notification,
)

app_name = 'notification-api'

urlpatterns = [
    path('', UserUnreadNotificationListAPIView.as_view(), name='unread-list-user'),
    path('all/', NotificationListAPIView.as_view(), name='list'),
    path('your-notification/', UserAllNotificationListAPIView.as_view(), name='all-list-user'),
    path('read/<int:pk>/', read_notification, name='read'),
    path('delete/<int:pk>/', delete_notification, name='delete'),
]