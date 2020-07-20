from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Post(models.Model):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Comment(models.Model):
    comment_content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Follow(models.Model):
    follower = models.ForeignKey(Follower, on_delete=models.CASCADE)
    following = models.ForeignKey(User, on_delete=models.CASCADE)
