from django_filters.rest_framework import FilterSet
from .models import Medicine, Category
import django_filters
from django.db.models import Case, When, BooleanField

class MedicineFilter(FilterSet):
    in_stock = django_filters.BooleanFilter(field_name='inventory', method='filter_in_stock', label='In Stock')

    class Meta:
        model = Medicine
        fields = {
            'category': ['exact'],
            'drug': ['exact'],
            'price': ['gt', 'lt'],
            'is_active': ['exact']
        }

    def filter_in_stock(self, queryset, name, value):
      if value:
          queryset = queryset.filter(inventory__gt=0)
      else:
          queryset = queryset.filter(inventory=0)
      return queryset
class CategoryFilter(FilterSet):
    class Meta:
        model = Category
        fields = {
            'general_category': ['exact'],
        }