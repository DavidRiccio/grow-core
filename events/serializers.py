from shared.serializers import BaseSerializer


class EventSerializer(BaseSerializer):
    """
    Serializador para instancias del modelo Event.

    Este serializador transforma una instancia de Event en un diccionario
    con los campos relevantes para su representación en una API.
    """

    def serialize_instance(self, instance) -> dict:
        """
        Serializa una instancia del modelo Event a un diccionario.

        Parameters
        ----------
        instance : Event
            Instancia del modelo Event que se desea serializar.

        Returns
        -------
        dict
            Diccionario con los datos serializados del evento, incluyendo:
            - 'id': Identificador único del evento.
            - 'name': Nombre del evento.
            - 'description': Descripción del evento.
            - 'date': Fecha del evento.
            - 'time': Hora del evento.
            - 'location': Ubicación del evento.
            - 'image': URL absoluta de la imagen del evento.
        """
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'date': instance.date,
            'time': instance.time,
            'location': instance.location,
            'image': f'{self.build_url(instance.image.url)}',
        }
