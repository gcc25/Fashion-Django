from django.contrib import admin
from .models import UserProfile, Wishlist


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'city', 'country']
    search_fields = ['user__username', 'user__email', 'phone']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'created', 'updated']
    search_fields = ['user__username', 'user__email']