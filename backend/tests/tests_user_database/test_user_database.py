import pytest
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserDatabase:
    def setup(self):
        self.api_client = APIClient()

    def test_aggregation_of_queries(self, create_admin):
        """Проверяем эндпоинт /api/v1/user_database/1/ на объединения GET запросов"""
        param = ["user_database", "resources", "enemies", "enemy_leaders"]
        admin = create_admin()
        self.api_client.force_authenticate(admin)
        response = self.api_client.get("/api/v1/user_database/1/")
        assert response.status_code == HTTP_200_OK
        for i in param:
            if i in response.data:
                # Проверяем на наличе словарей, может тут надо проверять на ключи?
                assert response.data["user_database"]
                assert response.data["resources"]
                assert response.data["enemies"]
                assert response.data["enemy_leaders"]
                break
