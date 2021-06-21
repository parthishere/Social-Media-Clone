from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from django.shortcuts import get_object_or_404, get_list_or_404
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
        if serializer.is_valid:
            user = serializer.save().user
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
 
 
 
@api_view(['POST',])
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
@permission_classes([AllowAny])
def retrive_profile(request, id):
    user_profile = get_object_or_404(UserProfile, id=id, active=True)
    serializer = UserProfileSerializer(user_profile, many=False)
    return Response(serializer.data)


class UserProfileListAPI(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [AllowAny,]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user__username', 'user__first_name', 'bio', 'name']
    ordering_fields = '__all__'

    def get_serializer_context(self, *args, **kwargs):
        return { "request":self.request }
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow_requested_user(request, id):
    """ Here *id* is requested user's *id* """
    self_profile = request.user.user_profile
    requested_user, user, added = self_profile.add_or_remove_to_following(id=id)
    
    serializer = UserProfileSerializer(self_profile, many=False)
    return Response(serializer.data)


@api_view(['GET', ])
@permission_classes([AllowAny])
def get_requested_user_following(request, id=None):
    """ using Reverse Queryset """
    requested_user = UserProfile.objects.get(id=id, active=True).user
    if requested_user is not None:
        following = requested_user.following
        serializer = UserProfileSerializer(following, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail':'no user profile found'}, status=status.HTTP_404_NOT_FOUND)
  
  
@api_view(['GET', ])
@permission_classes([AllowAny])
def get_requested_user_followers(request, id=None):
    requested_user_profile = UserProfile.objects.get(id=id, active=True)
    if requested_user_profile is not None:
        followers = requested_user_profile.followers
        serializer = UserSerilizer(followers, many=True)
        return Response(serializer.data)
    else:
        return Response({'detail':'no user profile found'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsOwnerOrReadOnly])
def delete_my_account(request):
    user = request.user
    user_profile = request.user.user_profile
    
    user_profile.delete()
    user.delete()
    return Response({'detail':'Account Deleted Successfully'}, status=status.HTTP_200_OK)


@api_view(['PATCH'])
@permission_classes((IsOwnerOrReadOnly))
def update_interests(request): 
    user_profile = request.user.userprofile
    interests = request.data
    user_profile.interests.set(
        TopicTag.objects.get_or_create(name=interest['name'])[0] for interest in interests
    )
    user_profile.save()
    serializer = UserProfileSerializer(user_profile, many=False)
    return Response(serializer.data)
 
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_post(request, pk=None):
    post = get_object_or_404(Post, pk=pk)
    data = {}
    user_profile = request.user.user_profile
    if post in user_profile.saved_posts.all():
        user_profile.saved_posts.remove(post)
        data['data'] = 'post removed from saved'
    else:
        user_profile.saved_posts.add(post)
        data['data'] = 'post added to saved'
        
    user_profile.save()
    
    return Response(data)
    


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_account(request):
    user = request.user
    user_profile = user.user_profile
    if user.is_authenticated and user_profile.follower_count >= 100:
        if user.post_user.count > 10 and (user_profile.timestamp[:4]-timezone.now()[:4]) >= 3:
            for post in user.post_user:
                post_like_count = post.likes.count()
            if post_like_count >= 1000:
                user_profile.verified = True
                user_profile.save()
            return Response({"data": "verified"})
    else:
        return Response({"data":"Not verified"})


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def recommended_user(request):
#     pass
   
   
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
