from django_filters.rest_framework import FilterSet
from .models import Medicine

class MedicineFilter(FilterSet):
  class Meta:
    model = Medicine
    fields = {
      'category': ['exact'],
      'price': ['gt', 'lt']
    }