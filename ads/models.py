from django.conf import settings
from django.db import models


class Advertisement(models.Model):
    title = models.CharField(max_length=200, verbose_name='Sarlavha')
    text = models.TextField(verbose_name='Matn')
    image_path = models.CharField(max_length=300, blank=True, null=True, verbose_name='Rasm')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Reklama'
        verbose_name_plural = 'Reklamalar'
        ordering = ['-id']

    def __str__(self):
        return self.title

    @property
    def image(self):
        if not self.image_path:
            return None
        if self.image_path.startswith('http'):
            return self.image_path
        if self.image_path.startswith(settings.MEDIA_URL.lstrip('/')):
            return f"{settings.BASE_URL}/{self.image_path}"
        return f"{settings.BASE_URL}/static/{self.image_path}"
