from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', related_name="watchlisted_by", blank=True)

class Listing(models.Model):
    title = models.CharField(max_length=64)
    details = models.TextField()
    starting_bid = models.IntegerField()
    picture = models.URLField(blank=True, null=True)

    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Furniture', 'Furniture'),
        ('Clothing', 'Clothing'),
        ('Fashion' , 'Fashion'),
        ('Other', 'Other'),
    ]
    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    bid_amount = models.IntegerField()

    def __str__(self):
        return f"Bid by {self.user} on {self.listing}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text}"
