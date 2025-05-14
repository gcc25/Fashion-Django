import django_filters
from .models import Product, Category, Color, Size

class ProductFilter(django_filters.FilterSet):
    SORT_CHOICES = (
        ('price', 'Price: Low to High'),
        ('-price', 'Price: High to Low'),
        ('-created', 'Newest First'),
        ('name', 'Name: A-Z'),
        ('-name', 'Name: Z-A'),
    )
    
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.ModelMultipleChoiceFilter(
        queryset=Category.objects.all(),
        field_name='category',
        label='Category'
    )
    sort = django_filters.ChoiceFilter(
        choices=SORT_CHOICES,
        method='filter_sort',
        label='Sort by'
    )
    
    class Meta:
        model = Product
        fields = ['category']
    
    def filter_sort(self, queryset, name, value):
        return queryset.order_by(value)