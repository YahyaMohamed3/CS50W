from django.contrib import admin
from .models import User, Listing, Bid, Comment


class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'starting_bid', 'is_active', 'user')

class BidAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'bid_amount')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('listing', 'user', 'text', 'created_at')

admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
