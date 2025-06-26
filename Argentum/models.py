from django.db import models
from django.conf import settings
from blog.models import Hub, Comment, Post

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profiles')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='user_profiles', null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='user_profiles', null=True, blank=True)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='user_profiles', null=True, blank=True)
    name = models.CharField(max_length=255)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name