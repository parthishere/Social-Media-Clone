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
                    remove_follower_view,
                    remove_following_view,
                    )

app_name = 'accounts'

urlpatterns = [
    path('follow-requests', follow_requested_user_list, name='followers-requests'),
    path('list/', UserSearchListView.as_view(), name='list'),
    
    
    path('<str:username>/update/', user_profile_update, name='update'),
    path('<str:username>/followers/', user_followers_list, name='user-followers'),
    path('<str:username>/followings/', user_following_list, name='user-following'),
    path('followers/remove/<str:username>/', remove_follower_view, name='remove-follower'),
    path('follow/<str:username>/', follow_unfollow_requested_user, name='follow-requested-user'),
    path('accept-request/<str:username>/', accept_follow_request_view, name='accept-request'),
    path('decline-request/<str:username>/', decline_follow_request_view, name='decline-request'),
    path('<str:username>/', UserProfileDetailView.as_view(), name='profile'),
]