from shared.serializers import BaseSerializer


class ProductSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'price': instance.price,
            'stock': instance.stock,
            'image': self.build_url(instance.image.url),
        }


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
