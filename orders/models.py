from django.conf import settings
from django.db import models

from products.models import Product

# Create your models here.


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'P', 'Pending'
        COMPLETED = 'C', 'Completed'
        CANCELLED = 'X', 'Cancelled'

    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
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
        for product in self.product.all():
            total += product.price
        return float(total)

    def increase_stock(self):
        for product in self.product.all():
            product.stock += 1
            product.save()

    def decrease_stock(self):
        for item in self.shoppingcartitem_set.all():
            item.product.stock -= item.quantity
            item.product.save()

    def add(self, product):
        self.product.add(product)
        self.save()

    def update_status(self, status):
        self.status = status
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.quantity}x {self.product.name} (Order {self.order.id})'

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
        for item in self.shoppingcartitem_set.all():
            item.product.stock -= item.quantity
            item.product.save()

    def add(self, product):
        self.product.add(product)
        self.save()
