from shared.serializers import BaseSerializer


class TokenSerializer(BaseSerializer):
    """
    Serializador para el modelo Token.

    Métodos
    -------
    serialize_instance(instance) -> dict
        Serializa una instancia de Token en un diccionario con su clave única.
    """

    def serialize_instance(self, instance) -> dict:
        """
        Serializa una instancia de token.

        Parameters
        ----------
        instance : Token
            Instancia del token a serializar.

        Returns
        -------
        dict
            Diccionario que representa la instancia del token con la clave 'key'.
        """
        return {'key': instance.key}


class ProfileSerializer(BaseSerializer):
    """
    Serializador para el modelo Profile.

    Métodos
    -------
    serialize_instance(instance) -> dict
        Serializa una instancia de Profile en un diccionario con sus atributos principales.
    """

    def serialize_instance(self, instance) -> dict:
        """
        Serializa una instancia de perfil.

        Parameters
        ----------
        instance : Profile
            Instancia del perfil a serializar.

        Returns
        -------
        dict
            Diccionario que representa la instancia del perfil, con las siguientes claves:
                - id : int
                - user : str
                - role : str
                - token : dict
        """
        return {
            'id': instance.user.id,
            'user': instance.user.username,
            'role': instance.role,
            'token': TokenSerializer(instance.user.token).serialize_instance(instance.user.token),
        }
