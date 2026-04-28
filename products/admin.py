from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category', 'status', 'is_top']
    list_filter = ['status', 'is_top', 'category']
    search_fields = ['name']
    list_editable = ['status', 'is_top']
