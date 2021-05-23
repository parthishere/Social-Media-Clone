from django.db import models
from django.contrib.auth.models import User

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