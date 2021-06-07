from rest_framework import serializers

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'first_name', 'last_name', 'username',
            'bio', 'email', 'role'
        )


class EmailSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField()


class TokenSerializer(serializers.Serializer):  # noqa
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    def validate(self, data):
        queryset = CustomUser.objects.filter(
            email=data.get('email'),
            confirmation_code=data.get('confirmation_code')
        )
        if queryset.exists():
            return queryset.first()
        raise serializers.ValidationError("Bad credentials")
