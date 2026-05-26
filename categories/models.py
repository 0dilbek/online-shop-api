from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.CASCADE, related_name='children'
    )
    unit_type = models.CharField(max_length=20, blank=True, default='piece')
    image_path = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} › {self.name}"
        return self.name

    @property
    def image(self):
        if not self.image_path:
            return None
        if self.image_path.startswith('http'):
            return self.image_path
        return f"{settings.BASE_URL}/static/{self.image_path}"

    @property
    def depth(self):
        d, node = 0, self.parent
        while node:
            d += 1
            node = node.parent
        return d
