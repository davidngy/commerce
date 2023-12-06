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
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    image = models.URLField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    comments = models.TextField(max_length=300, blank=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)



