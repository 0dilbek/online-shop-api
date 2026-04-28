from django.db import models

from customers.models import Customer
from products.models import Product


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_CONFIRMED = 'confirmed'
    STATUS_DELIVERING = 'delivering'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELED = 'canceled'
    STATUS_CHOICES = [
        (STATUS_NEW, 'Yangi'),
        (STATUS_CONFIRMED, 'Tasdiqlangan'),
        (STATUS_DELIVERING, 'Yetkazilmoqda'),
        (STATUS_COMPLETED, 'Yakunlangan'),
        (STATUS_CANCELED, 'Bekor qilingan'),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders'
    )
    customer_name = models.CharField(max_length=200)
    customer_phone = models.CharField(max_length=30)
    address = models.CharField(max_length=500)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_NEW)
    total_price = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} — {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    unit_price = models.IntegerField()  # so'm
    quantity = models.IntegerField(default=1)
    total_price = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Buyurtma elementi'
        verbose_name_plural = 'Buyurtma elementlari'

    def __str__(self):
        return f"OrderItem #{self.id} (order={self.order_id})"

    @property
    def image(self):
        if self.product:
            return self.product.image
        return None
