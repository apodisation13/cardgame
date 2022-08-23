import pytest
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework.test import APIClient

from apps.core.models import Faction

api_client = APIClient()


# ПЕРВЫЙ СПОСОБ - КЛАССАМИ
@pytest.mark.django_db
class TestModels:
    def setup(self):
        self.api_client = APIClient()

    def test_factions(self):
        # Тест метода __str__ у модели, он должен показать то, как бы она print()
        faction = Faction.objects.first()
        expected_result = "1 - Neutral"
        assert expected_result == faction.__str__()

    def test_faction_api(self, create_admin):
        # Тест эндпоинта фракций
        response = self.api_client.get("/api/v1/factions/")
        assert response.status_code == HTTP_401_UNAUTHORIZED
        admin = create_admin()  # поюзали фикстуру создания админа
        self.api_client.force_authenticate(admin)  # принудительно прошли аутентификацию
        # TODO: ну а вот тут надо дальше проверять


# Второй способ - функциями
# @pytest.mark.django_db
# def test_factions():
#     faction = Faction.objects.first()
#     expected_result = "1 - Neutral"
#     assert expected_result == faction.__str__()
#     factions = Faction.objects.all()
#     assert len(factions) == 4
#
