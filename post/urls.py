from django.urls import path, include

from .views import (
    PostCreateView,
    PostListView,
    like_post_view,
    PostUpdateView,
)

app_name = 'post'

urlpatterns = [
    # path('api/', include('post.api.urls')),
    path('', PostListView.is_view(), name='list'),
    path('<int:pk>/update', PostUpdateView.is_view(), name='update'),
    path('like/', like_post_view, name='like'),
]