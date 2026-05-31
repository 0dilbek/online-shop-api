from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'price', 'category_names', 'status', 'is_top']
    list_filter = ['status', 'is_top', 'categories']
    search_fields = ['name']
    list_editable = ['status', 'is_top']
    filter_horizontal = ['categories']

    def category_names(self, obj):
        return ', '.join(category.name for category in obj.categories.all())

    category_names.short_description = 'Kategoriyalar'
