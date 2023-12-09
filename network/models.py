from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    content = models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="post_author")
    date = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "user": self.user.username,
            "date": self.date.strftime("%b %d %Y, %I:%M %p"),
        }
    
    def number_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return f"{self.user}[{self.date}]:{self.content}"
    
class Follow(models.Model):
    user_following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_following")
    user_follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_follower")
    
    def serialize(self):
        return {
            "id_ing": self.user_following.id,
            "id_er": self.user_follower.id,
            "user_following": self.user_following.username,
            "user_follower": self.user_follower.username,
        }
     
    def __str__(self):
        return f"{self.user_following} is following by {self.user_follower}"

class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="liked_post")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_liked")
    
    '''def number_of_likes(self, post_id):
        count = self.post.filter(id=post_id).count
        return count'''

    def __str__(self):
        return f"{self.post} is liked by {self.user}"