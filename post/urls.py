from django.urls import path, include

from .views import (
    PostCreateView,
    PostListView,
    like_post_view,
    PostUpdateView,
    save_post_view,
    saved_posts_list_view,
    DeletePostView,
    LikedUserListView
)

app_name = 'post'

urlpatterns = [
    path('', PostListView.as_view(), name='list'),
    path('create/', PostCreateView.as_view(), name='create'),
    path('<int:pk>/update', PostUpdateView.as_view(), name='update'),
    path('<int:pk>/delete', DeletePostView.as_view(), name='delete'),
    path('like/', like_post_view, name='like'),
    path('<int:pk>/save', save_post_view, name='save'),
    path('<int:pk>/liked-user', LikedUserListView.as_view(), name='liked-user'),
    path('saved-list', saved_posts_list_view, name='saved-list'),
]