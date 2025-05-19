from shared.serializers import BaseSerializer


class ProductSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'price': instance.price,
            'stock': instance.stock,
            'image': f'http://localhost:8000v{self.build_url(instance.image.url)}',
        }
