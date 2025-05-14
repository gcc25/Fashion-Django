from django.contrib import admin
from .models import Category, Product, ProductImage, Size, Color

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 4

class SizeInline(admin.TabularInline):
    model = Size
    extra = 1

class ColorInline(admin.TabularInline):
    model = Color
    extra = 1

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'discount_price', 'category', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'discount_price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, SizeInline, ColorInline]
    search_fields = ['name', 'description']