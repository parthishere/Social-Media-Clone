
from django.urls import path, include

from .views import (
    PostListAPIView,
    PostCreate,
    UpdatePost,
    DeletePost,
    like_unlike_post,
    see_all_liked_user,
    self_posts,
    user_posts,
)

app_name = 'post-api'

urlpatterns = [
    path('list/', PostListAPIView.as_view(), name='list'),
    path('create/', PostCreate.as_view(), name='create'),
    path('update/<pk>', UpdatePost.as_view(), name='update'),
    path('delete/<pk>', DeletePost.as_view(), name='delete'),
    path('like/<pk>', like_unlike_post, name='like-post'),
    path('likes/list/<pk>', see_all_liked_user, name='likes-list'),
    path('list/your-posts', self_posts, name='your-posts'),
    path('user/<id>/', user_posts, name='user-post')
]