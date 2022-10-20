import pytest
from rest_framework.status import HTTP_200_OK, HTTP_401_UNAUTHORIZED, HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED
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
        self.api_client.logout()

    def test_api_user(self, create_user):
        """Проверка на доступ юзеру"""
        user = create_user()
        self.api_client.force_authenticate(user)
        print(user.username)
        response = self.api_client.get("/api/v1/factions/")
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_api_method(self, create_user):
        """Проверка на другие методы"""
        user = create_user()
        self.api_client.force_authenticate(user)
        response_post = self.api_client.post("/api/v1/factions/")
        response_delete = self.api_client.delete("/api/v1/factions/")
        assert response_post.status_code == HTTP_403_FORBIDDEN
        assert response_delete.status_code == HTTP_403_FORBIDDEN

    def test_api_faction(self, create_admin):
        """Проверка на полченные данные из эндпоинта фракций"""
        admin = create_admin()
        self.api_client.force_authenticate(admin)
        expected_result = 'Neutral'
        response = self.api_client.get("/api/v1/factions/")
        assert response.data[0]['name'] == expected_result
        assert len(response.data) == 4

    def test_get_game_const_admin(self, create_admin):
        """Проверка эндпоинта для админа"""
        admin = create_admin()
        self.api_client.force_authenticate(admin)
        response_admin = self.api_client.get("/api/v1/game_const/")
        assert response_admin.status_code == HTTP_200_OK

    def test_get_game_const_user(self, create_user):
        """Проверка эндпоинта для юсера"""
        user = create_user()
        self.api_client.force_authenticate(user)
        response_user = self.api_client.get("/api/v1/game_const/")
        assert response_user.status_code == HTTP_200_OK

    def test_game_const_other_methods(self, create_admin):
        """Проверка запрета на методы POST, DELETE"""
        admin = create_admin()
        self.api_client.force_authenticate(admin)
        response_post = self.api_client.post("/api/v1/game_const/")
        response_del = self.api_client.delete("/api/v1/game_const/")
        assert response_post.status_code == HTTP_405_METHOD_NOT_ALLOWED
        assert response_del.status_code == HTTP_405_METHOD_NOT_ALLOWED
