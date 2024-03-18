from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    def __str__(self):
        return self.name

# Image validator - cant be greater than 500 KB
def validate_image_size(value):
    filesize = value.size
    if filesize > 500 * 1024:  # 500 KB
        raise ValidationError("The maximum file size that can be uploaded is 500 KB.")

# Build listing module
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField(max_length=64)
    text = models.TextField(max_length=512)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='listing_images/', default='no_image.jpg', validators=[validate_image_size], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    current_highest_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='won_listings')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # Count bids
    def bid_count(self):
        return Bid.objects.filter(listing=self).count()
    def __str__(self):
        return self.title

# Build comments module
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='comments', default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'Comment by {self.user.username} on {self.created_at}'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}'s Watchlist"
    
class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)

    