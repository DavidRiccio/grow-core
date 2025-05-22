from services.serializers import ServiceSerializer
from shared.serializers import BaseSerializer

from .models import Booking


class BookingSerializer(BaseSerializer):
    """
    Serializador para una reserva.

    Attributes
    ----------
    None
    """

    def serialize_instance(self, instance) -> dict:
        """
        Serializa una instancia de reserva.

        Parameters
        ----------
        instance : Booking
            La instancia de reserva a serializar.

        Returns
        -------
        dict
            Un diccionario que representa la instancia de reserva, que contiene
            las siguientes claves:
                - id : int
                - user : int
                - service : dict
                - date : datetime
                - time_slot : dict
                - barber : str
                - barber_id : int
                - status : str
                - created_at : datetime
        """
        return {
            'id': instance.id,
            'user': instance.user.id,
            'service': ServiceSerializer(instance.service).serialize_instance(instance.service),
            'date': instance.date,
            'time_slot': TimeSlotSerializer(instance.time_slot).serialize_instance(
                instance.time_slot
            ),
            'barber': instance.barber.get_full_name(),
            'barber_id': instance.barber.id,
            'status': instance.get_status_display(),
            'created_at': instance.created_at,
        }


class TimeSlotSerializer(BaseSerializer):
    """
    Serializador para un bloque horario.

    Attributes
    ----------
    None
    """

    def serialize_instance(self, instance) -> dict:
        """
        Serializa una instancia de bloque horario.

        Parameters
        ----------
        instance : TimeSlot
            La instancia de bloque horario a serializar.

        Returns
        -------
        dict
            Un diccionario que representa la instancia de bloque horario, que contiene
            las siguientes claves:
                - id : int
                - start_time : datetime
                - end_time : datetime
        """
        return {
            'id': instance.id,
            'start_time': instance.start_time,
            'end_time': instance.end_time,
        }


class BookingEarningsSerializer(BaseSerializer):
    """
    Serializador para el resumen de ganancias de reservas.

    Attributes
    ----------
    None
    """

    def serialize_instance(self, instance=None) -> dict:
        """
        Serializa el resumen de ganancias de las reservas.

        Parameters
        ----------
        instance : Booking, opcional
            La instancia de reserva (no se utiliza en este método).

        Returns
        -------
        dict
            Un diccionario que contiene el resumen de ganancias con las siguientes claves:
                - daily_earnings : float
                - weekly_earnings : float
                - monthly_earnings : float
        """
        summary = Booking.earnings_summary()
        return {
            'daily_earnings': summary['daily'],
            'weekly_earnings': summary['weekly'],
            'monthly_earnings': summary['monthly'],
        }
