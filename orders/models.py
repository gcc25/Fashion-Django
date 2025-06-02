from django.db import models
from django.conf import settings
from typing import List, Optional
from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    first_name: str = models.CharField(max_length=50)
    last_name: str = models.CharField(max_length=50)
    email: str = models.EmailField()
    address: str = models.CharField(max_length=250)
    postal_code: str = models.CharField(max_length=20)
    city: str = models.CharField(max_length=100)
    country: str = models.CharField(max_length=100)
    phone: str = models.CharField(max_length=20)
    created: str = models.DateTimeField(auto_now_add=True)
    updated: str = models.DateTimeField(auto_now=True)
    status: str = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note: Optional[str] = models.TextField(blank=True)
    
    class Meta:
        ordering = ('-created',)
    
    def __str__(self) -> str:
        return f'Order {self.id}'
    
    def get_total_cost(self) -> float:
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order: Order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product: Product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price: float = models.DecimalField(max_digits=10, decimal_places=2)
    quantity: int = models.PositiveIntegerField(default=1)
    size: Optional[str] = models.CharField(max_length=20, blank=True, null=True)
    color: Optional[str] = models.CharField(max_length=50, blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.id)
    
    def get_cost(self) -> float:
        return self.price * self.quantity