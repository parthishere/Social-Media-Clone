from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.utils.text import slugify
from django.shortcuts import reverse, redirect
from time import timezone
import uuid

from .utils import random_string_generator
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from skills.models import Skill

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



class UserProfileManager(models.Manager):
    
    def get_or_new(self, request):
        obj = None
        created = False
        try: 
            qs = self.model.objects.filter(user=request.user)
        except Exception as e:
            print(e)
        if qs.count() == 1:
            obj = qs.first()
            created = False
        else:
            obj = self.model.objects.create(user=request.user)
            created = True
        return obj, created
    
    
    def add_or_remove_follower(self, request, user=None):
        if user.is_authenticated:
            try:
                user_obj = self.model.objects.get(user=user)
            except Exception as e:
                print(e)
            if user_obj.exists():
                if user in user_obj.follower.objects.all():
                    user_obj.follower.remove(user_obj)
                    user_obj.follower_count -= 1
                    user_obj.save()
                else:
                    user_obj.followers.add(user_obj)
                    user_obj.follower_count += 1
                    user_obj.save()
        return user_obj
    
    
    def add_or_remove_following(self, request, following_user=None):
        user = request.user
        try:
            user_obj = self.model.objects.get(user=user)
        except Exception as e:
            print(e) 
        if request.user.is_authenticated:
            if user in following_user.followers.objects.all():
                following_user.followers.remove(user)
                following_user.followers_count -= 1
                following_user.save()
            else:
                following_user.followers.add(user)
                following_user.followers_count += 1
                following_user.save()
                # Requested User and/ me who just clicked follow button 
        return following_user, user_obj
    
    
    def get_following_of_user(self, uuid):
        requested_user = self.model.get(id=uuid).user
        following_users = requested_user.following
        return following_users
    
    
    def get_followers_of_user(self, uuid):
        requested_user = self.model.get(id=uuid)
        followers = requested_user.followers
        return followers
        
                



class UserProfile(models.Model):
    id = models.UUIDField(default=uuid.uuid4,  unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_profile')
    name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_img = models.ImageField(upload_to='user/profiles',  blank=True, null=True)
    post_count = models.IntegerField(default=0)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    created = models.BooleanField(default=False)
    skill = models.CharField(max_length=100, null=True, blank=True)
    topic = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)  # we are gonna use it as archive account 
    
    objects = UserProfileManager()
    
    """
    profile = UserProfile.objects.first()
    profile.followers.all() -> All users following this profile
    user = request.user   -> Me
    user.following.all() -> All user profiles I follow
    """
    
    class Meta():
        ordering = ['-id']
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})
    
    # def check_verified(self):
    #     if self.user.is_authenticated and self.follower_count >= 100 and self.total_likes > 1000:
    #         if self.post > 10 and (self.timestamp[:4]-timezone.now()[:4]) >= 3:
    #             self.verified = True
    #             self.save()
    #             return True
    #     else:
    #         return False
        
    def return_skills(self):
        return self.skill
    
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
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"id": self.id})
        
    
    
def post_save_user_reciever(sender, created, instance, *args, **kwargs):
    if created:
        user = instance
        user_obj = UserProfile.objects.get_or_create(user=user)
        
        
post_save.connect(post_save_user_reciever, sender=User)



        
        
    