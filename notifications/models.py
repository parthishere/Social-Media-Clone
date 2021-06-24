from django.db import models
from django.contrib.auth.models import User
# Create your models here.

NOTIFICATION_CHOICES = {
    ('FOLLOW', 'FWO'),
    ('FOLLOWING', 'FWI'),
    ('POST', 'PS'),
    ('LIKE', 'LK'),
    ('COMMENT', 'COM'),
}

class Notification(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_user')
    to_user = models.ManyToManyField(User, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=5)