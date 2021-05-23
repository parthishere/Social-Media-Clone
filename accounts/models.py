from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed

from django.contrib.auth.models import User
from django.db.models.aggregates import Max

# Create your models here.





class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=True)
    name = models.CharField(max_length=100)
    bio = models.TextField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    profile_img = models.ImageField(upload_to='/user/profiles')
    post = models.FileField(upload_tp='user/post')
    followers = models.ManyToManyField(User, verbose_name='followers', null=True, blan=True)
    followers_count = models.IntegerField(default=0)
    created = models.BooleanField(default=False)
    skill = models.CharField(max_length=100, null=True, blank=True)
    topic = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=True)
    
    class Meta():
        ordering = ['-id']
    
    def __str__(self):
        return self.user.username
    
def post_save_user_reciever(sender, created, instance, *args, **kwargs):
    if created:
        user = instance
        UserProfile.object.get_or_create(user)
    