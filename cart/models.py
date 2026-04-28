from django.db import models

from products.models import Product


class Cart(models.Model):
    STATUS_OPEN = 'open'
    STATUS_ORDERED = 'ordered'
    STATUS_ABANDONED = 'abandoned'
    STATUS_CHOICES = [
        (STATUS_OPEN, 'Ochiq'),
        (STATUS_ORDERED, 'Buyurtma qilingan'),
        (STATUS_ABANDONED, 'Tark etilgan'),
    ]

    session_id = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Savat'
        verbose_name_plural = 'Savatlar'

    def __str__(self):
        return f"Cart #{self.id} ({self.status})"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    unit_price = models.IntegerField()  # so'm

    class Meta:
        verbose_name = 'Savat elementi'
        verbose_name_plural = 'Savat elementlari'

    def __str__(self):
        return f"CartItem #{self.id} (cart={self.cart_id})"

    @property
    def image(self):
        if self.product:
            return self.product.image
        return None
