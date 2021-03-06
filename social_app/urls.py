"""social_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/', include('allauth.urls')),
    
    path('api/users/', include('accounts.api.urls', namespace='accounts-api')),
    path('users/', include('accounts.urls', namespace='accounts')),
    
    path('api/posts/', include('post.api.urls', namespace='post-api')),
    path('post/', include('post.urls', namespace='post')),
    
    path('api/comments/', include('comments.api.urls', namespace='comment-api')),
    path('comments/', include('comments.urls', namespace='comments')),
    
    path('api/notifications/', include('notifications.api.urls', namespace='notification-api')),
    path('notifications/', include('notifications.urls', namespace='notification')),
    
    path('chat/', include('chat.urls', namespace='chat')),
    path('schema/', get_schema_view(
        title="MumbleAPI",
        description="API for the Social-Clone.dev",
        version="1.0.0"
    ), name="social-schema"),
    path('', include_docs_urls(
        title="SocialClone",
        description="API for the Social-Clone.dev",
    ), name="social-docs")
    # path('api/feed/', include('feed.api.urls', namespace='feed-api')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

