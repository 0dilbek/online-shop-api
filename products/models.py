from django.db import models
from django.conf import settings

from categories.models import Category


class Product(models.Model):
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_CHOICES = [
        (STATUS_ACTIVE, 'Faol'),
        (STATUS_INACTIVE, 'Nofaol'),
    ]

    name = models.CharField(max_length=200)
    price = models.IntegerField()  # so'm
    description = models.CharField(max_length=500, blank=True, null=True)
    image_path = models.CharField(max_length=300, blank=True, null=True)
    is_top = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='products')

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    def __str__(self):
        return self.name

    @property
    def image(self):
        if not self.image_path:
            return None
        if self.image_path.startswith('http'):
            return self.image_path
        return f"{settings.BASE_URL}/static/{self.image_path}"
