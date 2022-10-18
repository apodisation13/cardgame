from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND
from rest_framework.viewsets import GenericViewSet

from apps.accounts.models import CustomUser
from apps.accounts.serializers import LoginSerializer, UserSerializer


class CreateUserViewSet(GenericViewSet, mixins.CreateModelMixin):
    """Создание пользователя и хэшированного пароля"""
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email', None)
        is_email_used = CustomUser.objects.filter(email=email).exists()
        if is_email_used:
            print('мы тут')
            return HttpResponse("Такая почта уже занята", status=HTTP_400_BAD_REQUEST)
        password = data.get('password', None)
        request.data['password'] = make_password(password)
        return super().create(request, *args, **kwargs)


class LoginViewSet(GenericViewSet, mixins.CreateModelMixin):
    """Проверка почты и пароля"""

    queryset = CustomUser.objects.all()
    serializer_class = LoginSerializer
    permission_classes = []

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


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
        })
