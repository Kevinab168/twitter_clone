from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class TimeStampModel(models.Model):
    class Meta:
        abstract = True

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(TimeStampModel):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')


class Comment(TimeStampModel):
    comment_content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')


class Follow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')


class Image(models.Model):
    source = models.ImageField(upload_to='static/images/', null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
