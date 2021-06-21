from django.urls import path, include

from .views import (
    AddComment,
    comment_list_on_post,
    all_comment_list,
    UpdateComment,
    DeleteComment,
)

app_name = "comment-api"

urlpatterns = [
    path('create/', AddComment.as_view(), name='create'),
    path('list/<int:pk>/', comment_list_on_post, name='post-commnt'),
    path('list/all/', all_comment_list, name='list'),
    path('update/<int:pk>/', UpdateComment.as_view(), name='update'),
    path('delete/<int:pk>/', DeleteComment.as_view(), name='delete'),
]