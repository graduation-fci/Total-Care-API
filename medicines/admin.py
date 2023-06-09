from django.contrib import admin
from django.db.models.aggregates import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html, urlencode
from django.urls import reverse
from . import models

# Register your models here.

@admin.register(models.Drug)
class DrugAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    ordering = ['name']
    search_fields = ['name']
    list_filter = ['name']

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    ordering = ['name']
    search_fields = ['name']
    list_filter = ['name']

@admin.register(models.GeneralCategory)
class GeneralCategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    ordering = ['name']
    search_fields = ['name']
    list_filter = ['name']

@admin.register(models.Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ['__str__' , 'id','inventory','drugs_number']
    ordering = ['name']
    search_fields = ['name']
    autocomplete_fields = ['drug', 'category']
    @admin.display(ordering='drugs_number')
    def drugs_number(self, medicine):
        
        return ( medicine.drugs_number)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            drugs_number=Count('drug')
        )




    
