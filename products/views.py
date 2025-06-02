from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from typing import Any, Dict, Optional
from django.http import HttpRequest, HttpResponse

from .models import Category, Product
from .filters import ProductFilter
from cart.forms import CartAddProductForm


class ProductListView(ListView):
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Product.objects.filter(available=True)
        category_slug: Optional[str] = self.kwargs.get('category_slug')
        
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        search_query: Optional[str] = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) | 
                Q(description__icontains=search_query) |
                Q(meta_keywords__icontains=search_query)
            )
        
        self.filterset = ProductFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['filter'] = self.filterset
        
        category_slug: Optional[str] = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
        
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] = CartAddProductForm()
        context['related_products'] = Product.objects.filter(
            category=self.object.category
        ).exclude(id=self.object.id).order_by('?')[:4]
        return context


class FeaturedProductsListView(ListView):
    model = Product
    template_name = 'products/featured_products.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        return Product.objects.filter(featured=True, available=True)
    
    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context