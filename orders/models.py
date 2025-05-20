from django.conf import settings
from django.db import models


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        COMPLETED = 'C', 'Completed'
        CANCELLED = 'X', 'Cancelled'

    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    products = models.ManyToManyField('products.Product', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )

    def __str__(self):
        return f'{self.user} Status:{self.status}'

    @property
    def price(self):
        total = 0
        for product in self.products.all():
            total += product.price
        return float(total)

    def increase_stock(self):
        for product in self.products.all():
            product.stock += 1
            product.save()

    def decrease_stock(self):
        for product in self.products.all():
            product.stock -= 1
            product.save()

    def update_status(self, status):
        self.status = status
        self.save()

    def add(self, product):
        self.products.add(product)
        self.save()
