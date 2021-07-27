from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404, Http404
from time import timezone

from rest_framework import filters
from accounts.api.serializers import UserProfileSerializer, UserSerilizer
from accounts.models import UserProfile, User, TopicTag

from .permissions import IsOwnerOrReadOnly
from post.models import Post
from post.api.serializers import PostSerializer

        
@api_view(['GET',])
@permission_classes([IsOwnerOrReadOnly,])    
def get_self_profile(request):
    user = request.user.user_profile
    serializer = UserProfileSerializer(user, many=False)
    return Response(serializer.data)
    
    
class UpdateSelfProfile(APIView):
    queryset = UserProfile.objects.filter(active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    
    def patch(self, *args, **kwargs):
        user_profile = self.request.user.user_profile
        serializer = self.serializer_class(user_profile, data=self.request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            response = {'success': True, 'message': 'successfully updated your info',
                        'user': UserProfileSerializer(user).data}
            
            new_email = self.request.data.get('email')
            user = self.request.user
            if new_email is not None:
                user.email = new_email
                user_profile.email_verified = False
                user.save()
                user_profile.save()
            return Response(response, status=200)
        
        else:
            response = serializer.errors
            return Response(response, status=401)
        
class ImageUpdateAPIView(APIView):
    queryset = UserProfile.objects.filter(active=True)
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly,]
    
    def patch(self, *args, **kwargs):
        pass
 
 
 
@api_view(['PATCH',])
@permission_classes([IsOwnerOrReadOnly,])      
def delete_self_profile_img(request):
    user_profile = request.user.user_profile
    user = request.user
    try:
        user_profile.profile_pic = 'default.png'
        user_profile.save()
    
        response = { 'deleted': True, }
        return Response(response ,status=status.HTTP_200_OK)
    except:
        response = { 'deleted': False, }
        return Response(response ,status=status.HTTP_404_NOT_FOUND)
    

@api_view(['GET',])
@permission_classes([IsOwnerOrReadOnly,]) 
def get_self_followers(request):
    user_profile = request.user.user_profile
    followers = user_profile.followers.all()
    serializer = UserSerilizer(followers, many=True)
    return Response(serializer.data)


@api_view(['GET',])
@permission_classes([IsOwnerOrReadOnly,])    
def get_self_following(request):
    user_profile = request.user.user_profile
    following_users = request.user.following
    serializer = UserProfileSerializer(following_users, many=True)
    
    return Response(serializer.data)

@api_view(['GET',])
@permission_classes([AllowAny,])
def retrive_profile(request, username=None):
    user_profile = get_object_or_404(UserProfile, user__username=username, active=True)
    serializer = UserProfileSerializer(user_profile, many=False)
    return Response(serializer.data)


class UserProfileListAPI(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__first_name', 'bio', 'name', 'intrest']
    ordering_fields = '__all__'

    def get_serializer_context(self, *args, **kwargs):
        return { "request":self.request }
    
    
@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def follow_requested_user(request, username=None):
    """ Here *username* is requested user's *username* """
    
    user = request.user
    self_profile = request.user.user_profile
    try:
        user_to_follow_profile = UserProfile.objects.get(user__username=username)
    except Exception as e:
        print(e) 
    if request.user.is_authenticated:
        if request.user == user_to_follow_profile.user:
            raise Http404('You cant folllow you!')
        if user in user_to_follow_profile.followers.all():
            user_to_follow_profile.followers.remove(user)
            user_to_follow_profile.followers_count -= 1
            user_to_follow_profile.save()
            added = False
        elif user_to_follow_profile.private_account:
            user_to_follow_profile.followers_requests.add(user)
            user_to_follow_profile.save()
            added = False
        else:
            user_to_follow_profile.followers.add(user)
            user_to_follow_profile.followers_count += 1
            user_to_follow_profile.save()
            added = True
    
    
    serializer = UserProfileSerializer(self_profile, many=False)
    return Response(serializer.data)


@api_view(['POST',])
@permission_classes([IsOwnerOrReadOnly,])
def remove_user_from_followers(request, username=None):
    """ Here *username* is requested user's *username* """
    self_profile = request.user.user_profile
    user = request.user
    user_profile = user.user_profile
    
    requested_user = get_object_or_404(User, username=username)
    if request.user.is_authenticated:
        
        if requested_user in user_profile.followers.all():
            user_profile.followers.remove(requested_user)
            user_profile.save()

    
    serializer = UserProfileSerializer(self_profile, many=False)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([AllowAny,])
def get_requested_user_following(request, username=None):
    """ using Reverse Queryset """
    requested_user = UserProfile.objects.get(user__username=username, active=True).user
    if requested_user is not None:
        if requested_user.private_account:
            if request.user in requested_user.followers.all():
                following = requested_user.following
                serializer = UserProfileSerializer(following, many=True)
                return Response(serializer.data)
            else:
                Response({'detail':'user profile is private'}, status=status.HTTP_404_NOT_FOUND)
  
            
    else:
        return Response({'detail':'no user profile found'}, status=status.HTTP_404_NOT_FOUND)
  
  
@api_view(['GET', ])
@permission_classes([AllowAny,])
def get_requested_user_followers(request, username=None):
    requested_user_profile = UserProfile.objects.get(user__username=username, active=True)
    if requested_user_profile is not None:
        if requested_user_profile.private_account:
            if request.user in requested_user_profile.followers.all():
                followers = requested_user_profile.followers
                serializer = UserSerilizer(followers, many=True)
                return Response(serializer.data)
            else:
                Response({'detail':'user profile is private'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'detail':'no user profile found'}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['POST',])
@permission_classes([IsOwnerOrReadOnly,])
def delete_my_account(request):
    user = request.user
    user_profile = request.user.user_profile
    
    user_profile.delete()
    user.delete()
    return Response({'detail':'Account Deleted Successfully'}, status=status.HTTP_200_OK)


@api_view(['PATCH',])
@permission_classes((IsAuthenticated,))
def update_interests(request): 
    user_profile = request.user.user_profile
    intrests = request.data
    user_profile.intrest.set(
            TopicTag.objects.get_or_create(name=intrest['name']) for intrest in intrests
    )
    user_profile.save()
    serializer = UserProfileSerializer(user_profile, many=False)
    return Response(serializer.data)



from django.db.models import Count

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recommended_user(request):
    user = request.user
    user_qs = UserProfile.objects.filter(user=user)
    user_profile = request.user.user_profile
    users = User.objects.annotate(followers_count = Count('userprofile__followers')).order_by('followers_count').reverse().exclude(user=user)[0:5]  # reverse query of User count(model__field)
    for u in user.following.all():
        user_qs.append(u.following.first())
        if user_qs.count() > 10:
            break
            
    user_qs.exclude(user=user)
    
    serializer = UserProfileSerializer(user_qs, many=True)
    return Response(serializer.data)


@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def report_account(request, username=None):
    reported_user_profile = get_object_or_404(UserProfile, user__username=username)
    reported_user = reported_user_profile.user

    if request.user not in reported_user_profile.reported_by.all():
        reported_user_profile.add(request.user)
    else:
        reported_user_profile.remove(request.user)
        
    reported_user_profile.save()
        
    return Response()


@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def accept_follow_request(request, username=None):
    user = request.user
    requested_user_profile = UserProfile.objects.get(username=username)
    if requested_user_profile.private_account:
        if request.user in requested_user_profile.followers.all():
            if user in requested_user_profile.follow_requests.all():
                requested_user_profile.follow_requests.remove(user)
            else:
                pass
        elif user in requested_user_profile.follow_requests.all():
            requested_user_profile.followers.add(user)
            requested_user_profile.follow_requests.remove(user)
            
        return Response()
    else:
        return Response({"detail":"You can not accept follow request if you dont have private account"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def decline_follow_request(request, username=None):
    user = request.user
    requested_user_profile = UserProfile.objects.get(username=username)
    if request.user in requested_user_profile.followers.all():
        if user in requested_user_profile.follow_requests.all():
            requested_user_profile.follow_requests.remove(user)
        else:
            pass
    elif user in requested_user_profile.follow_requests.all():
        requested_user_profile.follow_requests.remove(user)
        
    return Response()
 

@api_view(['POST',])
@permission_classes([IsAuthenticated,])       
def change_to_private_account_view(request):
    user=request.user
    user_profile = user.user_profile
    if user_profile.private_account:
        user_profile.private_account = True
        user_profile.save()
        return Response({"detail": "Changed to Private account"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "already private"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        

@api_view(['POST',])
@permission_classes([IsAuthenticated,])
def change_to_open_account_view(request):
    user=request.user
    user_profile = user.user_profile
    if not user_profile.private_account:
        try:
            user_profile.followers.add(
                user for user in user_profile.followers_requests.all() 
            )
        except Exception as e:
            print(e)
        user_profile.save()
        return Response({"detail": "Changed to Open account"}, status=status.HTTP_200_OK)
    else:
        return Response({"detail": "already open"}, status=status.HTTP_406_NOT_ACCEPTABLE)


# class VerifyAccount(APIView):
    # serializer_class = UserProfile
    # permission_classes = [IsOwnerOrReadOnly]
    # queryset = UserProfile.objects.all()
    
    # def patch(self, *args, **kwargs):
    #     data = self.request.data
    #     user_profile =  self.request.user.user_profile
    #     # serializer = self.serializer_class(user_profile, data=data, partial=True)
    #     user_profile.

# @api_view(['PATCH'])
# @permission_classes([IsAuthenticated])
# def verify_account(request):
#     user = request.user
#     user_profile = user.user_profile
#     if user.is_authenticated and user_profile.follower_count >= 100:
#         if user.post_user.count > 10 and (user_profile.timestamp[:4]-timezone.now()[:4]) >= 3:
#             for post in user.post_user:
#                 post_like_count = post.likes.count()
#             if post_like_count >= 1000:
#                 user_profile.verified = True
#                 user_profile.save()
#             return Response({"data": "verified"})
#     else:
#         return Response({"data":"Not verified"})



   
   
# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# def send_activation_email(request):
#     user = request.user
#     user_profile = UserProfile.objects.get(user=user)
#     try:
#         mail_subject = 'Verify your account.'
#         message = render_to_string('verify-email.html', {
#             'user': user_profile,
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': default_token_generator.make_token(user),
#         })
#         to_email = user.email
#         email = EmailMessage(
#             mail_subject, message, to=[to_email]
#         )
#         email.send()
#         return Response('Mail sent Successfully',status=status.HTTP_200_OK)
#     except Exception as e:
#         return Response({'detail':f'{e}'},status=status.HTTP_403_FORBIDDEN)
    
       
      
# @api_view(['GET'])
# def activate(request, uidb64, token):
#     try:
#         uid = urlsafe_base64_decode(uidb64).decode()
#         user = User._default_manager.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     if user is not None and default_token_generator.check_token(user, token):
#         user_profile = UserProfile.objects.get(user=user)
#         user_profile.email_verified = True
#         user_profile.save()
#         return Response("Email Verified")
#     else:
#         return Response('Something went wrong , please try again',status=status.HTTP_406_NOT_ACCEPTABLE)
