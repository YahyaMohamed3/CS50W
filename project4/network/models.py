from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Posts(models.Model):
    user = models.ForeignKey(User , on_delete = models.CASCADE)
    content = models.TextField(null = False)
    date = models.DateField(auto_now_add = True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return f"{self.user.username}"

class Follow(models.Model):
    user = models.ForeignKey(User, related_name = "following" , on_delete = models.CASCADE)
    following = models.ManyToManyField(User , related_name = "followers")

    def __str__(self):
        return (f"{self.user.username} follows {self.following.count()} users and "
                f"is followed by {self.user.followers.count()} users")


