import uuid

from django.conf import settings
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        COMPLETED = 'C', 'Completed'
        CANCELLED = 'X', 'Cancelled'

    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    product = models.ManyToManyField(Product, related_name='orders', blank=True)

    def __str__(self):
        return f'{self.user} Status:{self.status}'

    @property
    def price(self):
        total = 0
        for product in self.product.all():
            total += product.price
        return float(total)

    def increase_stock(self):
        for product in self.product.all():
            product.stock += 1
            product.save()

    def decrease_stock(self):
        for product in self.product.all():
            product.stock -= 1
            product.save()

    def update_status(self, status):
        self.status = status
        self.save()

    def add(self, product):
        self.product.add(product)
        self.save()


class ShoppingCartItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
