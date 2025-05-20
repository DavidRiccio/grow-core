from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(
        upload_to='media/product_images/',
        default='product_images/no_product.png',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
