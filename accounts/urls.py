from django.urls import path

from .views import (
                    UserProfileDetailView,
                    UserSearchListView,
                    UpdateUserProfile,
                    user_followers_list,
                    user_following_list,
                    follow_unfollow_requested_user,
                    user_profile_update,
                    follow_requested_user_list,
                    accept_follow_request_view,
                    decline_follow_request_view,
                    
                    )

app_name = 'accounts'

urlpatterns = [
    path('list/', UserSearchListView.as_view(), name='list'),
    path('requests/', follow_requested_user_list, name='followers-requests'),
    path('<username>/', UserProfileDetailView.as_view(), name='profile'),
    path('<username>/update/', user_profile_update, name='update'),
    path('<username>/followers/', user_followers_list, name='user-followers'),
    path('<username>/followings/', user_following_list, name='user-following'),
    path('follow/<username>/', follow_unfollow_requested_user, name='follow-requested-user'),
    path('accept-request/<username>/', accept_follow_request_view, name='accept-request'),
    path('decline-request/<username>/', decline_follow_request_view, name='decline-request'),
]