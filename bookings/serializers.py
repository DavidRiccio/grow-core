from shared.serializers import BaseSerializer


class BookingSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'user': instance.user.id,
            'service': ServiceSerializer(instance.service).serialize_instance(instance.service),
            'barber': BarberSerializer(instance.barber).serialize_instance(instance.barber),
            'date': instance.date,
            'time': instance.time,
            'status': instance.status,
            'created_at': instance.created_at,
        }


class BarberSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'phone_number': instance.phone_number,
        }


class ServiceSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'price': str(instance.price),
        }
