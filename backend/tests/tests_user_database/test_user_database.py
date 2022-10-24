import pytest
from rest_framework.status import HTTP_200_OK
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserDatabase:
    def setup(self):
        self.api_client = APIClient()

    def test_aggregation_of_queries(self, create_user):
        """Проверяем эндпоинт /api/v1/user_database/1/ на объединения GET запросов"""
        key_user_database = ["user_database", "resources", "enemies", "enemy_leaders", "game_const"]
        user = create_user()
        self.api_client.force_authenticate(user)
        response = self.api_client.get("/api/v1/user_database/1/")
        assert response.status_code == HTTP_200_OK
        for key in key_user_database:
            assert key in response.data
