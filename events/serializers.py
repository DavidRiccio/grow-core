from shared.serializers import BaseSerializer


class EventSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'date': instance.date,
            'time': instance.time,
            'location': instance.location,
            'created_at': instance.created_at,
        }
