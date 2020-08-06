from django.contrib.auth.models import AbstractUser
from django.db import models

# Users
class User(AbstractUser):
    pass

# Items
class AuctionListing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(null=False)
    currentBid = models.FloatField(null=False)
    imgUrl = models.URLField(null=True, blank =True)
    category = models.CharField(max_length=100, null=True, blank =True)
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=100, null=True, blank =True)

    def __str__(self):
        return self.title

# Bids
class Bid(models.Model):
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.FloatField(null=False)

    def __str__(self):
        return str(self.value)


# Comments
class Comment(models.Model):
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=False)
    date = models.DateField()

    def __str__(self):
        return self.content

# Watchlist
class Watchlist(models.Model):
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    name = models.ForeignKey(User, on_delete=models.CASCADE)
    idNumber = models.IntegerField(null=False)

    def __str__(self):
        return self.item.title
