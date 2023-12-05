from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    categoryName = models.CharField(max_length=50)

class Listing(models.Model):    
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    image = models.URLField(blank=True)

class Bid(models.Model):
    bid = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User)
    category = models.ForeignKey(Category) 

class Comment(models.Model):
    bidder = models.ForeignKey(User)
    comments = models.TextField(max_length=300, blank=True)



