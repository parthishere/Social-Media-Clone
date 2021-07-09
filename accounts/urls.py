from django.urls import path

from .views import (
                    UserProfileDetailView,
                    UserSearchListView,
                    UpdateUserProfile,
                    user_followers_list,
                    user_following_list,
                    follow_unfollow_requested_user
                    )

app_name = 'accounts'

urlpatterns = [
    path('list/', UserSearchListView.as_view(), name='list'),
    path('<username>/', UserProfileDetailView.as_view(), name='profile'),
    path('<username>/update', UpdateUserProfile.as_view(), name='update'),
    path('<username>/followers', user_followers_list, name='user-followers'),
    path('<username>/followings', user_following_list, name='user-following'),
    path('follow/<username>', follow_unfollow_requested_user, name='follow-requested-user'),
]