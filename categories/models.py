from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    unit_type = models.CharField(max_length=20)  # "piece" yoki "weight"

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def __str__(self):
        return self.name
