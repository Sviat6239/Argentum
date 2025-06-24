from django.db import models
from autentification.models import User
from blog.models import Hub, Comment, Post

class UserProfile(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='Posts')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='Comments')
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='Hubs')
    name = models.CharField(max_length=255)
    fname = models.CharField(max_length=255)
    lname = models.CharField(max_length=255)
    bio = models.TextField()

    def __str__(self):
        return self.name