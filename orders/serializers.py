from products.serializers import ProductSerializer
from shared.serializers import BaseSerializer


class OrderSerializer(BaseSerializer):
    """
    Serializador para el modelo Order.

    Este serializador convierte instancias de la clase Order en diccionarios
    que pueden ser fácilmente convertidos a JSON.

    Parameters
    ----------
    instance : Order
        Instancia del modelo Order que se desea serializar.

    Attributes
    ----------
    request : HttpRequest
        Objeto de solicitud asociado para construir URLs completas si es necesario.

    Methods
    -------
    serialize_instance(instance)
        Serializa una instancia de Order a un diccionario.
    """

    def serialize_instance(self, instance) -> dict:
        """
        Serializa una instancia del modelo Order a un diccionario.

        Parameters
        ----------
        instance : Order
            Instancia del modelo Order.

        Returns
        -------
        dict
            Diccionario con los datos serializados de la orden.
        """
        return {
            'id': instance.id,
            'products': ProductSerializer(
                instance.products.all(), request=self.request
            ).serialize(),
            'price': instance.price,
            'created_at': instance.created_at,
            'status': instance.status,
        }
