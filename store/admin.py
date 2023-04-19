from django.contrib import admin

from . import models
from .models import OrderItem
# Register your models here.


class OrderItemInline(admin.TabularInline):
    # autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    model = OrderItem
    extra = 0

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['customer']
    inlines = [OrderItemInline]
    list_display = ['id', 'placed_at', 'customer']

# class InventoryFilter(admin.SimpleListFilter):
#     title = 'inventory'
#     parameter_name = 'inventory'

#     def lookups(self, request, model_admin):
#         return [
#             ('<10', 'Low')
#         ]

#     def queryset(self, request, queryset: QuerySet):
#         if self.value() == '<10':
#             return queryset.filter(inventory__lt=10)


