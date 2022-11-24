from rest_framework import serializers

from apps.accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password")


class LoginSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ("email", "password")


class AuthTokenResponseSerializer(serializers.Serializer):
    """Only for @extend_schema"""
    token = serializers.CharField()
    user_id = serializers.IntegerField()
    email = serializers.EmailField()
    username = serializers.CharField()
