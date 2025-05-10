from services.serializers import ServiceSerializer
from shared.serializers import BaseSerializer


class BookingSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'user': instance.user.id,
            'service': ServiceSerializer(instance.service).serialize_instance(instance.service),
            'date': instance.date,
            'time_slot': TimeSlotSerializer(instance.time_slot).serialize_instance(
                instance.time_slot
            ),
            'status': instance.status,
            'created_at': instance.created_at,
        }


class TimeSlotSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'start_time': instance.start_time,
            'end_time': instance.end_time,
        }
