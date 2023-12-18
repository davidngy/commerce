from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=100)

    def __str__(self):
        return self.categoryName


class Listing(models.Model):    
    title = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.CharField(max_length=200)
    image = models.URLField(blank=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")
    highestBidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="highestBidder")

    def __str__(self):
        return self.title

class Bid(models.Model):
    bid = models.IntegerField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True)


class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(max_length=300, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.commenter.username} - {self.listing.title}"

