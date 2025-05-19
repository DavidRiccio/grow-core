from shared.serializers import BaseSerializer


class TokenSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {'key': instance.key}


class ProfileSerializer(BaseSerializer):
    def serialize_instance(self, instance) -> dict:
        return {
            'id': instance.user.id,
            'user': instance.user.username,
            'role': instance.role,
            'token': TokenSerializer(instance.user.token).serialize_instance(instance.user.token),
        }
