from django.conf import settings
from django.db import models


class Order(models.Model):
    """
    Modelo que representa una orden de compra realizada por un usuario.

    Attributes
    ----------
    status : CharField
        Estado de la orden: Pendiente, Completada o Cancelada.
    products : ManyToManyField
        Lista de productos asociados a la orden.
    price : DecimalField
        Precio total de la orden (opcional).
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
    products = models.ManyToManyField('products.Product', blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
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
        return f'{self.user} Status:{self.status}'

    def add(self, product):
        """
        Agrega un producto a la orden y guarda los cambios en la base de datos.

        Parameters
        ----------
        product : Product
            Producto a añadir a la orden.
        """
        self.products.add(product)
        self.save()
