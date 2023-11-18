from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}[{self.date}]:{self.content}"