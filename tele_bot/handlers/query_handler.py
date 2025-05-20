from datetime import date, timedelta

from asgiref.sync import sync_to_async
from django.db import close_old_connections
from telegram import Update
from telegram.ext import CommandHandler, ContextTypes

from bookings.models import Booking
from services.models import Service

# ---------------------------
# 1. Handlers de Consultas
# ---------------------------


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejador del comando /start"""
    await update.message.reply_text(
        '✂️ Bienvenido a BarberBot!\n'
        'Comandos disponibles:\n'
        '/hoy - Ver citas de hoy\n'
        '/semana - Citas de esta semana\n'
        '/servicios - Listado de servicios'
    )


async def hoy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra las reservas de hoy"""
    try:
        reservas = await _get_reservas_hoy()
        response = _format_reservas(reservas, 'hoy') if reservas else '🗓️ No hay reservas para hoy'
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f'⚠️ Ha ocurrido un error: {e}')


async def semana(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra las reservas de la semana"""
    try:
        reservas = await _get_reservas_semana()
        response = (
            _format_reservas(reservas, 'esta semana')
            if reservas
            else '🗓️ No hay reservas esta semana'
        )
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f'⚠️ Ha ocurrido un error: {e}')


async def servicios(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Listado de servicios disponibles"""
    try:
        servicios = await _get_servicios()
        response = _format_servicios(servicios) if servicios else '⚠️ No hay servicios disponibles'
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f'⚠️ Ha ocurrido un error: {e}')


async def reservas_barbero(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Muestra las próximas reservas de un barbero específico."""
    if not context.args:
        await update.message.reply_text(
            '⚠️ Debes especificar el nombre o ID del barbero. Ejemplo: /reservas-barbero John'
        )
        return

    barber_name = ' '.join(
        context.args
    )  # Convertir los argumentos en el nombre completo del barbero

    try:
        reservas = await _get_reservas_barbero(barber_name)
        if not reservas:
            await update.message.reply_text(
                f'📭 No hay reservas próximas para el barbero "{barber_name}".'
            )
            return

        response = _format_reservas(reservas, f'próximas para {barber_name}')
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f'⚠️ Ha ocurrido un error: {e}')


# ---------------------------
# 2. Funciones de Soporte
# ---------------------------


@sync_to_async
def _get_reservas_hoy():
    close_old_connections()
    return list(
        Booking.objects.filter(date=date.today()).select_related('service', 'barber', 'time_slot')
    )


@sync_to_async
def _get_reservas_semana():
    close_old_connections()
    hoy = date.today()
    inicio_semana = hoy - timedelta(days=hoy.weekday())
    fin_semana = inicio_semana + timedelta(days=6)
    return list(
        Booking.objects.filter(date__range=[inicio_semana, fin_semana]).select_related(
            'service', 'barber', 'time_slot'
        )
    )


@sync_to_async
def _get_reservas_barbero(barber_name):
    close_old_connections()
    return list(
        Booking.objects.filter(
            barber__full_name__icontains=barber_name, date__gte=date.today()
        ).select_related('service', 'barber', 'time_slot')
    )


@sync_to_async
def _get_servicios():
    close_old_connections()
    return list(Service.objects.all())


def _format_reservas(reservas, periodo):
    header = f'📌 Reservas de {periodo} ({date.today()}):\n'
    reservas_formateadas = []
    for booking in reservas:
        service_name = booking.service.name if booking.service else 'Servicio no especificado'
        barber_name = booking.barber.get_full_name() if booking.barber else 'Barbero no asignado'

        # Asumiendo que time_slot tiene un campo start_time tipo TimeField
        if booking.time_slot and hasattr(booking.time_slot, 'start_time'):
            time_slot_str = booking.time_slot.start_time.strftime('%H:%M')
        else:
            time_slot_str = 'Hora no especificada'

        reservas_formateadas.append(
            f'• {booking.date} {time_slot_str} - {service_name} con {barber_name}'
        )
    return header + '\n'.join(reservas_formateadas)


def _format_servicios(servicios):
    header = '🔧 Servicios disponibles:\n'
    return header + '\n'.join(
        f'- {service.name} ({service.price}€) - Duración: {service.duration}\n'
        for service in servicios
    )


# ---------------------------
# 3. Registro de Handlers
# ---------------------------

start_handler = CommandHandler('start', start)
hoy_handler = CommandHandler('hoy', hoy)
semana_handler = CommandHandler('semana', semana)
servicios_handler = CommandHandler('servicios', servicios)
reservas_barbero_handler = CommandHandler('reservas', reservas_barbero)
