from django.utils.crypto import get_random_string
from rest_framework import serializers

from users.models import CustomUser


class ConfCodeSerializer(serializers.ModelSerializer):
    pass


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(default=get_random_string())

    class Meta:
        model = CustomUser
        fields = '__all__'
