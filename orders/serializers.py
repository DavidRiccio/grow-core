from shared.serializers import BaseSerializer


class CartItemSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'user': instance.user.id,
            'product': instance.product.id,
            'quantity': instance.quantity,
        }


class OrderSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'user': instance.user.id,
            'items': instance.product.id,
            'total_price': instance.total_price,
            'created_at': instance.created_at,
            'status': instance.status,
        }
