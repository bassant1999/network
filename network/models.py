from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def serialize(self):
        return {
            "id": self.id,
            "Username":self.username
        }



class Post(models.Model):
    content = models.CharField(max_length=400)
    date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner", null=True)
    likes = models.IntegerField()
    def __str__(self):
        return f"{self.content} ({self.likes}) ({self.date})"

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "date": self.date,
            "owner": (self.owner).serialize(),
            "likes": self.likes
        }

class Like(models.Model):
    Lowner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lowner", null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post", null=True)

class Follow(models.Model):
    userF = models.ForeignKey(User, on_delete=models.CASCADE, related_name="userF", null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fowner", null=True)