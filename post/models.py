from django.db import models
from django.contrib.auth.models import User


class PostManager(models.Manager):
    
    def show_likes_by_followings(self,request,post=None):
        user = request.user
        likes_by_followings = []
        if user.is_authenticated:
            try:
                user_obj = self.model.objects.get(user=user)
            except Exception as e:
                print(e) 
            following_user = user_obj.return_following
            for u in list(post.likes.objects.all()):
                if u in following_user:
                   likes_by_followings.append(u)
        return likes_by_followings 
                    
            
            

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post/images')
    likes = models.ForeignKey(User, verbose_name='liked_user', on_delete=models.CASCADE, null=True, blank=True)
    like_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta():
        ordering = ['-id']