from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_name', 'unit_price', 'quantity', 'total_price']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_phone', 'status', 'total_price', 'created_at']
    list_filter = ['status']
    search_fields = ['customer_name', 'customer_phone']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [OrderItemInline]
