from django.contrib.auth.hashers import make_password
from django.db import models


class User(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'A', 'ADMIN'
        WORKER = 'W', 'WORKER'
        CLIENT = 'C', 'CLIENT'

    username = models.CharField(max_length=128, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    role = models.CharField(choices=Role.choices, max_length=1, default=Role.CLIENT)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.username}'

    def save(self, *args, **kwargs):
        if not self.pk:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
