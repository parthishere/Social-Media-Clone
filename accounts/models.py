from django.db import models
from django.shortcuts import Http404
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.utils.text import slugify
from django.shortcuts import reverse, redirect, get_object_or_404
from time import timezone
import uuid
from rest_framework.reverse import reverse as api_reverse

from .utils import random_string_generator
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
import post.models

# Create your models here.
# def unique_slug_generator_for_user_profile(instance, new_slug=None):
    
#     if new_slug is not None:
#         slug = new_slug
#     else:
#         slug = slugify(instance.user.username)

#     Klass = instance.__class__
#     qs_exists = Klass.objects.filter(slug=slug).exists()
#     if qs_exists:
#         new_slug = "{slug}-{randstr}".format(
#                     slug=slug,
#                     randstr=random_string_generator(size=4)
#                 )
#         return unique_slug_generator_for_user_profile(instance, new_slug=new_slug)
#     return slug

class TopicTag(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name



class UserProfileManager(models.Manager):
    
    def remove_follower(self, request, username=None):
        user = request.user
        user_profile = self.__class__.objects.get(user=user)
        
        requested_user = get_object_or_404(User, username=username)
        if request.user.is_authenticated:
            
            if requested_user in user_profile.following.all():
                user_profile.following.remove(requested_user)
                user_profile.save()
                
        return requested_user
    
    
    def add_or_remove_to_following(self, request, username=None):
        user = request.user
        added = False
        try:
            user_to_follow_profile = self.__class__.objects.get(user__username=username)
        except Exception as e:
            print(e) 
        if request.user.is_authenticated:
            if request.user == user_to_follow_profile.user:
                raise Http404('You cant folllow you!')
            if user in user_to_follow_profile.followers.objects.all():
                user_to_follow_profile.followers.remove(user)
                user_to_follow_profile.followers_count -= 1
                user_to_follow_profile.save()
                added = False
            else:
                user_to_follow_profile.followers.add(user)
                user_to_follow_profile.followers_count += 1
                user_to_follow_profile.save()
                added = True
                # Requested User and/ me who just clicked follow button 
        return user_to_follow_profile, user, added
    
    
    def get_following_of_user(self, username=None):
        requested_user = self.__class__.objects.get(user__username=username).user
        following_users = requested_user.following
        return following_users
    
    
    def get_followers_of_user(self, username=None):
        requested_user = UserProfile.objects.get(user__username=username)
        followers = requested_user.followers
        return followers
        
                



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_img = models.ImageField(upload_to='user/profiles',  blank=True, null=True)
    post_count = models.IntegerField(default=0)
    private_account = models.BooleanField(default=False)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    followers_requests = models.ManyToManyField(User, related_name='follow_requested', blank=True)
    blocked_users = models.ManyToManyField(User, related_name='blocked_user_profile', blank=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    created = models.BooleanField(default=False)
    intrest = models.ManyToManyField(TopicTag, related_name='profile_intrest', blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)  # we are gonna use it as archive account 
    email_verified = models.BooleanField(default=False)
    saved_posts = models.ManyToManyField('post.Post', blank=True)
    reported_by = models.ManyToManyField(User, related_name='reported_accounts', blank=True)
    report_count = models.IntegerField(default=0)
    
    
    objects = UserProfileManager()
    
    """
    profile = UserProfile.objects.first()
    profile.followers.all() -> All users following this profile
    user = request.user   -> Me
    user.following.all() -> All user profiles I follow
    """
    
    class Meta():
        ordering = ['-id']
        
    def __unicode__(self):
        return self.id
    
    def __str__(self):
        return self.user.username + " | " + str(self.id)
    
    # def check_verified(self):
    #     if self.user.is_authenticated and self.follower_count >= 100 and self.total_likes > 1000:
    #         if self.post > 10 and (self.timestamp[:4]-timezone.now()[:4]) >= 3:
    #             self.verified = True
    #             self.save()
    #             return True
    #     else:
    #         return False
        
    @property
    def return_skills(self):
        return self.skill
    
    @property
    def return_topic(self):
        return self.topic
    
    # def total_likes(self):
    #     pass
    
    def get_following(self):
        user = self.user
        following_userprofile = user.following
        return following_userprofile
    
    def get_self_posts(self):
        user = self.user
        posts = user.post_user
        return posts
        
    def get_self_comments(self):
        comments = self.user.comment_user
        return comments
    
    def get_self_liked_posts(self):
        liked_posts = self.user.liked_user
        return liked_posts
    
    @property
    def account_type(self):
        return self.private_account
    
    
    def get_api_url(self, request=None):
        return api_reverse('account-api:profile-detail', kwargs={"username": self.user.username}, request=request)
        
    
    
def post_save_user_reciever(sender, created, instance, *args, **kwargs):
    if created:
        user = instance
        user_obj = UserProfile.objects.get_or_create(user=user)
        
        
post_save.connect(post_save_user_reciever, sender=User)




def pre_save_userprofile_reciever(sender, instance, *args, **kwargs):
    user_profile = instance
    user = user_profile.user
    user_profile.followers_count = user_profile.followers.all().count()
    
    for u in user_profile.followers.all():
        u.user_profile.followers_count = u.user_profile.followers.all().count()
        u.user_profile.following_count = u.following.all().count()
        
    for u_req in user.following.all():
        u_req.followers_count = u_req.followers.all().count()
        u_req.following_count = u_req.user.following.all().count()
        
    user_profile.following_count = user.following.all().count()
        
        
pre_save.connect(pre_save_userprofile_reciever, sender=UserProfile)



        
        
    