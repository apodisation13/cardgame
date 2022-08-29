import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_405_METHOD_NOT_ALLOWED
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestModels:
    def setup(self):
        self.api_client = APIClient()

    def test_api_endpoint_faction(self):
        """Проверка эндпоинта фракций"""
        response = self.api_client.get("/api/v1/factions/")
        assert response.status_code == HTTP_401_UNAUTHORIZED

    def test_api_admin(self, create_admin):
        """Проверка на доступ админу"""
        admin = create_admin()
        self.api_client.force_authenticate(admin)
        response = self.api_client.get("/api/v1/factions/")
        assert response.status_code == HTTP_200_OK

    def test_api_user(self, create_user):
        """Проверка на доступ юзеру"""
        user = create_user()
        self.api_client.force_authenticate(user)
        response = self.api_client.get("/api/v1/factions/")
        assert response.status_code == HTTP_200_OK

    # def test_api_token(self, create_admin):
    #     """Проверка на токен"""
    #     admin = create_admin()
    #     self.api_client.force_authenticate(admin)
    #     rep = self.api_client.post("/accounts/api-token-auth/", data={"username": "kopljjj4444@yandex.ru",
    #                                                                   "password": "Qwerty1111"})
    #     response = self.api_client.get("/accounts/api-token-auth/")
    #     print(rep.data)

    def test_api_method(self, create_user):
        """Проверка на другие методы"""
        user = create_user()
        self.api_client.force_authenticate(user)
        response_post = self.api_client.post("/api/v1/factions/")
        response_delete = self.api_client.delete("/api/v1/factions/")  # Не уверен, что надо проверять
        assert response_post.status_code == HTTP_405_METHOD_NOT_ALLOWED
        assert response_delete.status_code == HTTP_405_METHOD_NOT_ALLOWED

    def test_api_faction(self, create_admin):
        """Проверка на полченные данные из эндпоинта фракций"""
        admin = create_admin()
        self.api_client.force_authenticate(admin)
        expected_result = 'Neutral'
        response = self.api_client.get("/api/v1/factions/")
        response_data = response.data
        data = response_data[0]
        assert dict(data)['name'] == expected_result
        assert len(response_data) == 4
