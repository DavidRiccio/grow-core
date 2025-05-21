# signals.py
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_related_models(sender, instance, created, **kwargs):
    """
    Crea modelos relacionados al usuario después de que se guarda una instancia de usuario.

    Este receptor se activa después de que se guarda un nuevo usuario. Si el usuario
    es creado, se generan automáticamente un perfil y un token de autenticación para él.

    Parameters
    ----------
    sender : Model
        El modelo que envía la señal (en este caso, el modelo de usuario).
    instance : User
        La instancia del usuario que se ha guardado.
    created : bool
        Indica si la instancia fue creada (True) o actualizada (False).
    kwargs : dict
        Argumentos adicionales que pueden ser pasados a la señal.
    """
    if created:
        Profile.objects.create(user=instance)
        Token.objects.create(user=instance)
