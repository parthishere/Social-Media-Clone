from post.models import Post
from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.utils.text import slugify
from django.shortcuts import reverse, redirect
from time import timezone

from .utils import random_string_generator
from django.contrib.auth.models import User
from django.db.models.aggregates import Max

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
    
    def get_liked_posts(request):
        user = request.user
        post_count = 0
        if user.is_authenticated:
            qs = Post.objects.filter(likes=user)
            for obj in qs:
                post_count +=1
            return qs, post_count
        

                



class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=True)
    slug = models.SlugField(blank=True, null=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    profile_img = models.ImageField(upload_to='/user/profiles',  blank=True, null=True)
    post_count = models.IntegerField(default=0)
    followers = models.ManyToManyField(User, verbose_name='followers', null=True, blank=True)
    followers_count = models.IntegerField(default=0)
    created = models.BooleanField(default=False)
    skill = models.CharField(max_length=100, null=True, blank=True)
    topic = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    verified = models.BooleanField(default=False)
    saved   = models.ManyToManyField(Post, blank=True, null=True)
    
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
        
    
    
def post_save_user_reciever(sender, created, instance, *args, **kwargs):
    if created:
        user = instance
        UserProfile.object.get_or_create(user=user)
        
post_save.connect(post_save_user_reciever, sender=User)

def pre_save_user_profile_reciever(sender, instance, *arsgs, **kwargs):
    if not instance.slug:
        slug = unique_slug_generator_for_user_profile(instance)
        instance.slug = slug
        instance.created = True

        
        
    