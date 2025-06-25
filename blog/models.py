from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation

class Category(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['title']

class Tag(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=60)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ['title']

class Hub(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=320)
    description = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='hubs')
    categories = models.ManyToManyField(Category, related_name='hubs', blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Hub"
        verbose_name_plural = "Hubs"
        ordering = ['-created_at', 'title']

class Discussion(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    title = models.CharField(max_length=320)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='discussions')
    content = models.TextField()
    tags = models.ManyToManyField(Tag, related_name='discussions', blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='discussions')
    created_at = models.DateTimeField(default=timezone.now)
    votes = GenericRelation('Vote')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Discussion"
        verbose_name_plural = "Discussions"
        ordering = ['-created_at', 'title']

class Post(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    hub = models.ForeignKey(Hub, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField(Tag, related_name='posts')
    title = models.CharField(max_length=320)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(default=timezone.now)
    votes = GenericRelation('Vote')

    def __str__(self):
        return self.title

    @property
    def vote_count(self):
        return sum(vote.value for vote in self.votes.all() if vote.value) or 0

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ['-created_at', 'title']

class Comment(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    content = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(default=timezone.now)
    votes = GenericRelation('Vote')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)

    def __str__(self):
        return f"{self.author.username} - {self.content[:30]}"

    @property
    def vote_count(self):
        return sum(vote.value for vote in self.votes.all() if vote.value) or 0

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['-created_at']

class Vote(models.Model):
    VOTE_TYPES = (
        (1, 'Upvote'),
        (-1, 'Downvote'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='votes')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    value = models.IntegerField(choices=VOTE_TYPES)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')
        verbose_name = "Vote"
        verbose_name_plural = "Votes"

    def __str__(self):
        return f"{self.user.username} {self.get_value_display()} on {self.content_object}"