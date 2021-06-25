from django.urls import path

from .views import (
    NotificationListAPIView,
    UserNotificationListAPIView,
    read_notification,
    delete_notification,
)

app_name = 'notification-api'

userpatterns = [
    path('', UserNotificationListAPIView),
]