from products.serializers import ProductSerializer
from shared.serializers import BaseSerializer


class OrderSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'products': ProductSerializer(
                instance.products.all(), request=self.request
            ).serialize(),
            'price': instance.price,
            'created_at': instance.created_at,
            'status': instance.status,
        }
