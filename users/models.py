import uuid

from django.conf import settings
from django.db import models


class Profile(models.Model):
    """
    Modelo que representa el perfil extendido de un usuario, incluyendo su rol en el sistema.

    Atributos
    ----------
    user : OneToOneField
        Relación uno a uno con el usuario del sistema.
    role : CharField
        Rol del usuario, que puede ser ADMIN, WORKER o CLIENT.
    created_at : DateTimeField
        Fecha y hora de creación del perfil.
    updated_at : DateTimeField
        Fecha y hora de la última actualización del perfil.

    Clases internas
    ---------------
    Role : TextChoices
        Enumeración de los roles disponibles:
            - 'A' (ADMIN)
            - 'W' (WORKER)
            - 'C' (CLIENT)

    Métodos
    -------
    __str__ : str
        Devuelve una representación legible del perfil (nombre de usuario).
    """

    class Role(models.TextChoices):
        """
        Enumeración de los roles posibles en el sistema.
        """

        ADMIN = 'A', 'ADMIN'
        WORKER = 'W', 'WORKER'
        CLIENT = 'C', 'CLIENT'

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile'
    )
    role = models.CharField(choices=Role.choices, max_length=1, default=Role.CLIENT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Retorna una representación legible del perfil.

        Returns
        -------
        str
            Username asociado al perfil.
        """
        return f'{self.user}'


class Token(models.Model):
    """
    Modelo que representa un token de autenticación único asociado a un usuario.

    Atributos
    ----------
    user : OneToOneField
        Relación uno a uno con el usuario del sistema.
    key : UUIDField
        Token único generado automáticamente para el usuario.
    created_at : DateTimeField
        Fecha y hora de creación del token.

    Métodos
    -------
    __str__ : str
        Devuelve una representación legible del token (nombre de usuario).
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='token'
    )
    key = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Retorna una representación legible del token.

        Returns
        -------
        str
            Username asociado al token.
        """
        return f'{self.user}'
