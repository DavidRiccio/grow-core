from datetime import timedelta

from django.conf import settings
from django.db import models
from django.db.models import Sum
from django.utils.timezone import now


class Order(models.Model):
    """
    Modelo que representa una orden de compra realizada por un usuario.

    Attributes
    ----------
    status : CharField
        Estado de la orden: Pendiente, Completada o Cancelada.
    price : DecimalField
        Precio total de la orden (calculado automáticamente).
    created_at : DateTimeField
        Fecha y hora de creación de la orden.
    updated_at : DateTimeField
        Fecha y hora de la última actualización.
    user : ForeignKey
        Usuario que realizó la orden.

    Notes
    -----
    Utiliza una enumeración interna `Status` para los estados válidos:
        - 'P': Pending
        - 'C': Completed
        - 'X': Cancelled
    """

    class Status(models.TextChoices):
        """
        Enumeración de los estados posibles de una orden.

        Attributes
        ----------
        PENDING : str
            Orden pendiente ('P').
        COMPLETED : str
            Orden completada ('C').
        CANCELLED : str
            Orden cancelada ('X').
        """

        PENDING = 'P', 'Pending'
        COMPLETED = 'C', 'Completed'
        CANCELLED = 'X', 'Cancelled'

    status = models.CharField(max_length=1, choices=Status.choices, default=Status.PENDING)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )

    def __str__(self):
        """
        Retorna una representación legible de la orden.

        Returns
        -------
        str
            Cadena con el nombre del usuario y el estado de la orden.
        """
        return f'{self.user} - Order #{self.id} - Status: {self.get_status_display()}'

    def calculate_total(self):
        """
        Calcula y actualiza el precio total de la orden basado en los items.
        
        Returns
        -------
        Decimal
            El precio total calculado.
        """
        total = sum(item.get_total_price() for item in self.items.all())
        self.price = total
        return total

    @classmethod
    def earnings_summary(cls):
        """
        Calcula los ingresos totales por órdenes completadas en distintos periodos.

        Returns
        -------
        dict
            Diccionario con las llaves `'daily'`, `'weekly'` y `'monthly'` indicando
            el total de ingresos en cada periodo.
        """
        today = now().date()
        start_week = today - timedelta(days=today.weekday())
        start_month = today.replace(day=1)

        daily = (
            cls.objects.filter(created_at__date=today, status=cls.Status.COMPLETED).aggregate(
                total=Sum('price')
            )['total']
            or 0
        )

        weekly = (
            cls.objects.filter(
                created_at__date__gte=start_week, 
                created_at__date__lte=today, 
                status=cls.Status.COMPLETED
            ).aggregate(total=Sum('price'))['total']
            or 0
        )

        monthly = (
            cls.objects.filter(
                created_at__date__gte=start_month, 
                created_at__date__lte=today, 
                status=cls.Status.COMPLETED
            ).aggregate(total=Sum('price'))['total']
            or 0
        )

        return {'daily': daily, 'weekly': weekly, 'monthly': monthly}



class OrderItem(models.Model):
    """
    Modelo que representa un item específico dentro de una orden.
    
    Almacena la información detallada de cada producto en una orden,
    incluyendo cantidad y precio unitario al momento de la compra.
    
    Attributes
    ----------
    order : ForeignKey
        Referencia a la orden que contiene este item.
    product : ForeignKey
        Producto asociado a este item.
    quantity : PositiveIntegerField
        Cantidad del producto en la orden.
    unit_price : DecimalField
        Precio unitario del producto al momento de la compra.
        Esto preserva el precio histórico independientemente de
        cambios futuros en el precio del producto.
    """
    
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        """
        Sobrescribe el método save para asignar automáticamente 
        el precio del producto como unit_price.
        """
        if not self.unit_price:
            self.unit_price = self.product.price
        super().save(*args, **kwargs)
    
    class Meta:
        unique_together = ('order', 'product')
    
    def __str__(self):
        """
        Retorna una representación legible del item de orden.
        
        Returns
        -------
        str
            Cadena con información del producto, cantidad y precio.
        """
        return f'{self.product.name} x{self.quantity} @ ${self.unit_price}'
    
    @property
    def subtotal(self):
        """
        Calcula el subtotal de este item.
        
        Returns
        -------
        Decimal
            Precio unitario multiplicado por la cantidad.
        """
        return self.unit_price * self.quantity