from shared.serializers import BaseSerializer


class BookingSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'user': instance.user.id,
            'service': ServiceSerializer(instance.service).serialize_instance(instance.service),
            'date': instance.date,
            'time': instance.time,
            'status': instance.status,
            'created_at': instance.created_at,
        }


class ServiceSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'price': str(instance.price),
        }
