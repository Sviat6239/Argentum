from django.db import models
from autentification.models import CustomUser  
from blog.models import Hub, Comment, Post

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='userprofile')
    post = models.ForeignKey(Post, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profiles')
    comment = models.ForeignKey(Comment, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profiles')
    hub = models.ForeignKey(Hub, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_profiles')
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.name or self.user.username