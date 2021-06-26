from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import pre_save, post_save

from comments.models import Comment
from post.models import Post
from accounts.models import User, UserProfile
# Create your models here.

NOTIFICATION_CHOICES = (
    ('follow', 'follow'),
    ('post', 'post'),
    ('like', 'like'),
    ('comment', 'comment'),
    ('recomment', 'recomment'),
)



class Notification(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user')
    to_user = models.ForeignKey(User,  on_delete=models.CASCADE, related_name='notification_to_user', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=10)
    follow = models.ForeignKey(User, related_name='follow_notification_user', blank=True, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_notification', blank=True, null=True, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='comment_notification', blank=True, null=True, on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    created = models.BooleanField(default=True)
    content = models.TextField(default="You have notification", max_length=255)
    
    def __str__(self):
        return self.notification_type + ' | from : ' +self.from_user.username 
    
    
def post_notification_post_save(sender, instance, created, **kwargs):
    if created:
        from_user = instance.user
        to_users = instance.user.user_profile.followers.all()
        for to_user in to_users:
            Notification.objects.create(
                                        from_user=from_user,
                                        to_user=to_user,
                                        notification_type='post',
                                        content=f"{instance.user.username} posted picture !",
                                        post=instance,
                                        )
    
post_save.connect(post_notification_post_save, sender=Post)



def comment_notification_post_save(sender, instance, created, **kwargs):
    if created:
        from_user = instance.user
        to_user = instance.post.user
        Notification.objects.create(
                                    from_user=from_user,
                                    to_user=to_user,
                                    notification_type='post',
                                    content=f"{instance.user.username} liked on your picture !",
                                    comment=instance,
                                    )
    
post_save.connect(comment_notification_post_save, sender=Comment)




def like_notification_post_save(sender, instance, created, **kwargs):
    if not created:
        from_user = instance.likes.first()
        to_user = instance.user
        Notification.objects.create(
                                    from_user=from_user,
                                    to_user=to_user,
                                    notification_type='like',
                                    content=f"{to_user.username} liked your picture !",
                                    post=instance,
                                    )
    
post_save.connect(like_notification_post_save, sender=Post)
  
    
    
    
def follow_notification_post_save(sender, instance, created, **kwargs):
    if not created:
        from_user = instance.followers.all().first()
        to_user = instance.user
        Notification.objects.create(
                                    from_user=from_user,
                                    to_user=to_user,
                                    notification_type='follow',
                                    content=f"{from_user.username} just followed you",
                                    follow=instance.user,
                                    )

post_save.connect(follow_notification_post_save, sender=UserProfile)