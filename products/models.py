from django.db import models
from django.urls import reverse
from typing import Optional


class Category(models.Model):
    name: str = models.CharField(max_length=100)
    slug: str = models.SlugField(max_length=100, unique=True)
    description: str = models.TextField(blank=True)
    image: str = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True)
    
    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self) -> str:
        return reverse('products:product_list_by_category', args=[self.slug])


class Product(models.Model):
    category: Category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name: str = models.CharField(max_length=200)
    slug: str = models.SlugField(max_length=200, unique=True)
    description: str = models.TextField(blank=True)
    price: float = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price: Optional[float] = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    available: bool = models.BooleanField(default=True)
    created: str = models.DateTimeField(auto_now_add=True)
    updated: str = models.DateTimeField(auto_now=True)
    featured: bool = models.BooleanField(default=False)
    meta_keywords: str = models.CharField(max_length=255, blank=True, help_text='Comma separated keywords for SEO')
    meta_description: str = models.TextField(blank=True, help_text='Description for SEO')
    
    class Meta:
        ordering = ('-created',)
        indexes = [models.Index(fields=['id', 'slug'])]
    
    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self) -> str:
        return reverse('products:product_detail', args=[self.slug])
    
    def get_discount_percent(self) -> int:
        if self.discount_price:
            return int(100 - (self.discount_price * 100) / self.price)
        return 0


class ProductImage(models.Model):
    product: Product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image: str = models.ImageField(upload_to='products/%Y/%m/%d')
    alt_text: str = models.CharField(max_length=200, blank=True)
    is_main: bool = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f"Image for {self.product.name}"


class Size(models.Model):
    product: Product = models.ForeignKey(Product, related_name='sizes', on_delete=models.CASCADE)
    name: str = models.CharField(max_length=20)
    available: bool = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name


class Color(models.Model):
    product: Product = models.ForeignKey(Product, related_name='colors', on_delete=models.CASCADE)
    name: str = models.CharField(max_length=50)
    code: str = models.CharField(max_length=10, help_text='Color HEX code')
    available: bool = models.BooleanField(default=True)
    
    def __str__(self) -> str:
        return self.name