from shared.serializers import BaseSerializer


class ProfileSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.id,
            'user': instance.user,
            'created_at': instance.created_at,
            'updated_at': instance.updated_at,
        }
