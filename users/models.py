from django.db import models
from django.conf import settings
from typing import Optional
from products.models import Product


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    phone: Optional[str] = models.CharField(max_length=20, blank=True)
    address: Optional[str] = models.CharField(max_length=250, blank=True)
    city: Optional[str] = models.CharField(max_length=100, blank=True)
    postal_code: Optional[str] = models.CharField(max_length=20, blank=True)
    country: Optional[str] = models.CharField(max_length=100, blank=True)
    
    def __str__(self) -> str:
        return f'Profile for {self.user.username}'


class Wishlist(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wishlist')
    products = models.ManyToManyField(Product, related_name='wishlists', blank=True)
    created: str = models.DateTimeField(auto_now_add=True)
    updated: str = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return f'Wishlist for {self.user.username}'