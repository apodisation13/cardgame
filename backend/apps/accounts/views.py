from django.contrib.auth.hashers import make_password
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.viewsets import GenericViewSet

from apps.accounts.models import CustomUser
from apps.accounts.serializers import LoginSerializer, UserSerializer


class CreateUserViewSet(GenericViewSet, mixins.CreateModelMixin):
    """Создание пользователя и хэшированного пароля"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        password = data.get('password', None)
        request.data['password'] = make_password(password)
        return super().create(request, *args, **kwargs)


class LoginViewSet(GenericViewSet, mixins.CreateModelMixin):
    """Проверка почты и пароля"""

    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        email = data.get('email', None)
        password = data.get('password', None)
        u = CustomUser.objects.filter(email=email).first()
        if u:
            if u.check_password(password):
                return Response(status=HTTP_200_OK)
            return Response(status=HTTP_401_UNAUTHORIZED)
        return Response(status=HTTP_404_NOT_FOUND)
