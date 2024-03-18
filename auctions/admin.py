from django.contrib import admin
from .models import Category, Listing, Comment, Watchlist, Bid

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Comment)
admin.site.register(Watchlist)
admin.site.register(Bid)

