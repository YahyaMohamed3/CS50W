from django.contrib import admin
from .models import User, Posts, Follow

# Custom User Admin to display additional fields if needed
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active')
    search_fields = ('username', 'email')

# Register User model
admin.site.register(User, UserAdmin)

# Register Posts model
class PostsAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'date', 'likes_count')  # Change this line

    def likes_count(self, obj):
        return obj.likes.count()  # Return the count of likes
    likes_count.short_description = 'Likes'  # Set a short description for the column

admin.site.register(Posts, PostsAdmin)


# Register Follow model
class FollowAdmin(admin.ModelAdmin):
    list_display = ('user',)
    search_fields = ('user__username',)  # Search by username of the user

admin.site.register(Follow, FollowAdmin)
