from django_filters.rest_framework import FilterSet
from .models import Order
import django_filters

class OrderFilter(FilterSet):

    year = django_filters.NumberFilter(field_name='placed_at', lookup_expr='year')

    class Meta:
        model = Order
        fields = ['customer','order_status','year']

