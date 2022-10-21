from apps.accounts.models import CustomUser
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("email", "password")
