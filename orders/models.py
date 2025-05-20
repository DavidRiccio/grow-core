from django.conf import settings
from django.core.exceptions import ValidationError
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
        return float(sum(product.price for product in self.products.all()))

    def _update_stock(self, increment: bool):
        """Actualiza el stock de los productos y valida disponibilidad."""
        for product in self.products.all():
            if not increment and product.stock < 1:
                raise ValidationError(f'Stock insuficiente para {product.name}')
            product.stock += 1 if increment else -1
            product.save()

    def confirm_order(self):
        """Confirma la orden, disminuye el stock y actualiza el estado."""
        if self.status != self.Status.PENDING:
            raise ValidationError('La orden ya fue procesada.')
        self._update_stock(increment=False)
        self.status = self.Status.COMPLETED
        self.save()

    def cancel_order(self):
        """Cancela la orden y restaura el stock."""
        if self.status != self.Status.COMPLETED:
            raise ValidationError('Solo se pueden cancelar órdenes completadas.')
        self._update_stock(increment=True)
        self.status = self.Status.CANCELLED
        self.save()

    def add(self, product):
        self.products.add(product)
        self.save()
