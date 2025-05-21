from shared.serializers import BaseSerializer


class ProductSerializer(BaseSerializer):
    """
    Serializador para el modelo Product.

    Métodos
    -------
    serialize_instance(instance) -> dict
        Serializa una instancia de Product en un diccionario con sus atributos principales.
    """

    def serialize_instance(self, instance) -> dict:
        """
        Serializa una instancia de producto.

        Parameters
        ----------
        instance : Product
            Instancia del producto a serializar.

        Returns
        -------
        dict
            Diccionario que representa la instancia del producto, con las siguientes claves:
                - id : int
                - name : str
                - description : str or None
                - price : Decimal
                - stock : int
                - image : str (URL completa de la imagen)
        """
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'price': instance.price,
            'stock': instance.stock,
            'image': f'http://localhost:8000{self.build_url(instance.image.url)}',
        }
