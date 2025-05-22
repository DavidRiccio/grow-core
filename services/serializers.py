from shared.serializers import BaseSerializer


class ServiceSerializer(BaseSerializer):
    """
    Serializador para el modelo Service.

    Métodos
    -------
    serialize_instance(instance) -> dict
        Serializa una instancia de Service en un diccionario con sus atributos principales.
    """

    def serialize_instance(self, instance) -> dict:
        """
        Serializa una instancia de servicio.

        Parameters
        ----------
        instance : Service
            Instancia del servicio a serializar.

        Returns
        -------
        dict
            Diccionario que representa la instancia del servicio, con las siguientes claves:
                - id : int
                - name : str
                - description : str or None
                - duration : timedelta
                - price : str
                - created_at : datetime
                - image : str (URL completa de la imagen)
        """
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'duration': instance.duration,
            'price': str(instance.price),
            'created_at': instance.created_at,
            'image': f'{self.build_url(instance.image.url)}',
        }
