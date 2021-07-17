from django.db import models

from django.contrib.auth.models import User
from post.models import Post

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment_post')
    text = models.TextField(default='Cool✨')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    likes = models.ForeignKey(User, related_name='comment_liked_user', on_delete=models.CASCADE, null=True, blank=True)
    like_count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.user.username
    
    class Meta():
        ordering = ['-id']
        
    