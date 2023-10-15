from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

    def __str__(self):
        return f"{self.username}"

class Categories(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.title}"

class Listings(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    photo = models.URLField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_user")
    is_active = models.BooleanField()
    id_categories = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="listing_categories")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_owner", blank=True, null=True)

    def __str__(self):
        return f"{self.title}"

class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="comments_listing")
    comment = models.CharField(max_length=1500)

    def __str__(self):
        return f"{self.author}:{self.listing}"    

class Bids(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="bids_listing")
    price = models.IntegerField()
    is_current=models.BooleanField()

    def __str__(self):
        return f"{self.author}:{self.listing}" 

class Watchlist(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name="watchlist_listing")
    
    def __str__(self):
        return f"{self.author}:{self.listing}" 
    