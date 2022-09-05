import pytest
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestModels:
    def setup(self):
        self.api_client = APIClient()

    def test_login_post(self, create_admin):
        """Проверка на токен пользователя"""
        admin = create_admin()
        data = {"username": admin.email, "password": "VEry-1-strong-test-passWorD"}
        response = self.api_client.post("/accounts/api-token-auth/", data=data, format="json")
        token = Token.objects.filter(user=admin).first()
        response_token = response.data['token']
        assert token.key == response_token
