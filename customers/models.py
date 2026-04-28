from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Customer(models.Model):
    full_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=30, unique=True)
    hashed_password = models.CharField(max_length=255)
    default_address = models.CharField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Mijoz'
        verbose_name_plural = 'Mijozlar'

    def __str__(self):
        return f"{self.full_name} ({self.phone})"

    def set_password(self, raw: str) -> None:
        self.hashed_password = make_password(raw)

    def verify_password(self, raw: str) -> bool:
        return check_password(raw, self.hashed_password)
