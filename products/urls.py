from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.FeaturedProductsListView.as_view(), name='featured_products'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('category/<slug:category_slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    path('product/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
]