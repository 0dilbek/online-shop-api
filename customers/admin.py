from django.contrib import admin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'phone', 'default_address', 'created_at']
    search_fields = ['full_name', 'phone']
    readonly_fields = ['hashed_password', 'created_at']
