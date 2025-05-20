# bookings/tasks.py
from django.conf import settings
from django.core.mail import send_mail
from django_rq import job


@job('default')
def send_booking_confirmation(user_email, service_name, date, time_slot):
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
