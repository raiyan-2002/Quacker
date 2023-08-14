from django.contrib.auth.models import AbstractUser
from django.db import models
import django.utils.timezone

class User(AbstractUser):
    user_id = models.AutoField(primary_key=True, editable=False)
    posts = models.ManyToManyField('Post', blank=True, related_name = "liked_posts")
    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    post_id = models.AutoField(primary_key=True, editable=False)
    likes = models.IntegerField(default=0)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=django.utils.timezone.now())
    content = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.post_id}: {self.content} by {self.creator}"

class Follower(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    following_list = models.ManyToManyField(User, blank=True, related_name='followers')

    def __str__(self):
        all_following = self.following_list.all()
        return f"{self.user} follows {all_following}"