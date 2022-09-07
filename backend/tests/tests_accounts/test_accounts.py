import pytest
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestModels:
    def test_login_post(self, create_admin, api_client):
        """Проверка на токен пользователя"""
        admin = create_admin()
        data = {"username": admin.email, "password": "VEry-1-strong-test-passWorD"}
        response = api_client.post("/accounts/api-token-auth/", data=data, format="json")
        token = Token.objects.filter(user=admin).first()
        response_token = response.data['token']
        assert token.key == response_token
