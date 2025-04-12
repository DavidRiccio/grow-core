from shared.serializers import BaseSerializer


class UserSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'email': instance.email,
            'phone_number': instance.phone_number,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
