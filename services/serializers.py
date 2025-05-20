from shared.serializers import BaseSerializer


class ServiceSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'duration': instance.duration,
            'price': str(instance.price),
            'created_at': instance.created_at,
            'image': f'{self.build_url(instance.image.url)}',
        }
