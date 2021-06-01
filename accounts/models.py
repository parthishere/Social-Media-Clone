from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.utils.text import slugify
from django.shortcuts import reverse, redirect
from time import timezone

from .utils import random_string_generator
from django.contrib.auth.models import User
from django.db.models.aggregates import Max
from skills.models import Skill

# Create your models here.
def unique_slug_generator_for_user_profile(instance, new_slug=None):
    
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.user.username)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator_for_user_profile(instance, new_slug=new_slug)
    return slug


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
    
    def return_followers(self, request):
        user = request.user
        if request.user.is_authenticated:
            try:
                user_obj = self.model.objects.get(user=user)
            except Exception as e:
                print(e)
            return user_obj.followers.objects.all()
        
    
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
                
            
        
    def return_following(self, request):
        following = []
        qs = User.objects.filter(active=True)
        user = request.user
        try:
            user_obj = self.model.objects.get(user=user)
        except Exception as e:
            print(e)
        for obj in qs.followers.all():
            if user_obj.user == obj:
                following += obj
                user_obj.following_count += 1
                user_obj.save()
        return following, user_obj
    
    
    
        

                



class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=100, blank=True, null=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_img = models.ImageField(upload_to='user/profiles',  blank=True, null=True)
    post_count = models.IntegerField(default=0)
    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    created = models.BooleanField(default=False)
    skill = models.CharField(max_length=100, null=True, blank=True)
    topic = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    
    objects = UserProfileManager()
    
    class Meta():
        ordering = ['-id']
    
    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("model_detail", kwargs={"slug": self.slug})
    
    def check_verified(self):
        if self.user.is_authenticated and self.follower_count >= 100 and self.total_likes > 1000:
            if self.post > 10 and (self.timestamp[:4]-timezone.now()[:4]) >= 3:
                self.verified = True
                self.save()
                return True
        else:
            return False
        
    def return_skills(self):
        return self.skill
    
    def return_topic(self):
        return self.topic
    
    def total_likes(self):
        total_like = 0
        for p in self.post:
            total_like += p.like
        return total_like
    
    def get_absolute_url(self):
        #return reverse("model_detail", kwargs={"pk": self.pk})
        pass
        
    
    
def post_save_user_reciever(sender, created, instance, *args, **kwargs):
    if created:
        user = instance
        user_obj = UserProfile.objects.get_or_create(user=user)
        
        # if user_obj.skills:
        #     list_of_skills = String(user_obj.skills)
        #     for skill in list_of_skills:
        #         if Skill.objects.filter(skill=skill):
        #             pass
        #         else:
        #             Skill.objects.create(skill=skill)
        
post_save.connect(post_save_user_reciever, sender=User)

def pre_save_user_profile_reciever(sender, instance, *arsgs, **kwargs):
    if not instance.slug:
        slug = unique_slug_generator_for_user_profile(instance)
        instance.slug = slug
        instance.created = True
        
pre_save.connect(pre_save_user_profile_reciever, sender=UserProfile)

        
        
    