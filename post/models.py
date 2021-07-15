from django.db import models
from django.contrib.auth.models import User
from image_cropping import ImageRatioField
import uuid


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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_user')
    image = models.ImageField(upload_to='post/images')
     # size is "width x height"
    cropping = ImageRatioField('image', '430x360')
    caption = models.TextField(default='feeling good ✔🎶')
    likes = models.ManyToManyField(User, related_name='liked_user', blank=True)
    like_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    objects = PostManager()
    
    def __str__(self):
        return self.user.username
    
    class Meta():
        ordering = ['-id']
        
    def get_absolute_url(self):
        #return reverse("model_detail", kwargs={"pk": self.pk})
        pass
    
