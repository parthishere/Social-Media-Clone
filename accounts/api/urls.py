from django.urls import path, include

from .views import (
    get_self_profile,
    UpdateSelfProfile, 
    ImageUpdateAPIView,
    delete_self_profile_img,
    get_self_followers,
    get_self_following,
    retrive_profile,
    UserProfileListAPI,
    follow_requested_user,
    get_requested_user_followers,
    get_requested_user_following,
    delete_my_account,
    update_interests,
    # verify_account,
    remove_user_from_followers,
    recommended_user,

)

app_name = 'account-api'

urlpatterns = [

    path('your-profile/', get_self_profile, name='self-profile'),
    path('update-profile/', UpdateSelfProfile.as_view(), name='update-profile'),
    path('delete-image/', delete_self_profile_img, name='delete-img'),
    path('your-followers/', get_self_followers, name='your-followers'),
    path('your-following/', get_self_following, name='your-following'),
    path('<str:username>/', retrive_profile, name='profile-detail'),
    path('', UserProfileListAPI.as_view(), name='profile-list'),
    path('follow/<str:username>/', follow_requested_user, name='follow-profile'),
    path('remove-following/<str:username>/', remove_user_from_followers, name='remove-following'),
    path('user-followers/<str:username>/', get_requested_user_followers, name='user-followers'),
    path('user-following/<str:username>/', get_requested_user_following, name='user-following'),
    path('delete-profile/', delete_my_account, name='delete-profile'),
    path('intrests/update', update_interests, name='update-intrest'),
    path('recommended-users/', recommended_user, name='recommended-user'),
    # path('verify/', verify_account, name='verify-account'),
    # path('/', ProfileListAPIView.as_view(), name='profile_list'),
    # path('list/', ProfileListAPIView.as_view(), name='profile_list'),
]