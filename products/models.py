from django.db import models


class Product(models.Model):
    """
    Modelo que representa un producto disponible para la venta.

    Atributos
    ----------
    name : CharField
        Nombre del producto.
    description : TextField
        Descripción opcional del producto.
    price : DecimalField
        Precio del producto, con hasta 8 dígitos y 2 decimales.
    stock : PositiveIntegerField
        Cantidad disponible en inventario.
    image : ImageField
        Imagen del producto. Puede ser personalizada o usar una imagen por defecto.

    Métodos
    -------
    __str__ : str
        Devuelve el nombre del producto como representación legible.
    """

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to='media/product_images/',
        default='products_images/no_product.png',
        blank=True,
        null=True,
    )

    def __str__(self):
        """
        Retorna una representación legible del producto.

        Returns
        -------
        str
            Nombre del producto.
        """
        return self.name
