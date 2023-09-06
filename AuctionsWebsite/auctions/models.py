from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(max_length=191,blank = False,unique = True)
    password = models.CharField(max_length=9,blank = False)
    email = models.EmailField(primary_key = True, unique = True)
    

    def __str__(self):
      return "{}".format(self.email)

class Category(models.Model):
    cat_name = models.CharField(max_length=100,blank = False)

    def __str__(self):
        return f"{self.cat_name}"


class Auction_listing(models.Model):
    title = models.CharField(max_length=191,blank = False,unique = True)
    image = models.CharField(max_length=191,blank = True)
    content = models.CharField(max_length=500,blank = True)
    date= models.DateTimeField(blank = True) 
    starting_value = models.IntegerField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE, related_name = "user")
    category = models.ForeignKey(Category, null = True, related_name = "listings", on_delete = models.PROTECT)
    isActive = models.BooleanField(max_length=100,unique = False)
    watchlist = models.ManyToManyField(User,blank = True, related_name = "listingwatchlist")

    def __str__(self):
        return f"{self.title}: {self.content}"

class Bid(models.Model):
    bid_value = models.IntegerField()
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name = "user_bids")
    auction_listing = models.ForeignKey(Auction_listing, null = True, blank = True,on_delete=models.CASCADE,related_name = "bids")    

    def __str__(self):
        return f"{self.bid_value}: {self.created_by}"


class Comment(models.Model):
    auction_listing = models.ForeignKey(Auction_listing, null = True, blank = True,on_delete=models.CASCADE,related_name = "comments")
    comment = models.CharField(max_length=500,blank = True)
    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name='comments')


    def __str__(self):
        return f"{self.comment} -by {self.created_by.username}"



