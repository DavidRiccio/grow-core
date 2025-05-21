# bookings/tasks.py
from django.conf import settings
from django.core.mail import send_mail
from django_rq import job


@job('default')
def send_booking_confirmation(user_email, service_name, date, time_slot):
    """
    Envía un correo electrónico de confirmación de reserva.

    Esta función es una tarea encolada que envía un email al usuario
    confirmando los detalles de su reserva.

    Parameters
    ----------
    user_email : str
        Correo electrónico del usuario que realizó la reserva.
    service_name : str
        Nombre del servicio reservado.
    date : str
        Fecha de la reserva.
    time_slot : str
        Horario reservado en formato cadena.
    """
    subject = 'Confirmación de reserva'
    message = f"""
    ¡Tu reserva ha sido confirmada!
    
    Servicio: {service_name}
    Fecha: {date}
    Horario: {time_slot}
    
    Gracias por elegirnos.
    """
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False,
    )
