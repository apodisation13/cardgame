import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK

from apps.core.models import Faction


api_client = APIClient()


# TODO: ВНИМАНИЕ!!!!!!!
# FIXME: ВРЕМЕННО НАДО ЗАКОММЕНТИТЬ СТРОКИ 42-43 в accounts/utils.py


# ПЕРВЫЙ СПОСОБ - КЛАССАМИ
@pytest.mark.django_db
class TestModels:
    def setup(self):
        self.api_client = APIClient()

    def test_factions(self):
        faction = Faction.objects.first()
        expected_result = "1 - Neutral"
        assert expected_result == faction.__str__()

    def test_faction_api(self, create_admin):
        faction = Faction.objects.first()
        expected_result = "1 - Neutral"
        assert expected_result == faction.__str__()
        response = self.api_client.get("/api/v1/factions/")
        assert response.status_code == HTTP_401_UNAUTHORIZED
        admin = create_admin()
        self.api_client.force_authenticate(admin)
        response = self.api_client.get("/api/v1/factions/")
        assert response.status_code == HTTP_200_OK


# Второй способ - функциями
# @pytest.mark.django_db
# def test_factions():
#     faction = Faction.objects.first()
#     expected_result = "1 - Neutral"
#     assert expected_result == faction.__str__()
#     factions = Faction.objects.all()
#     assert len(factions) == 4
#
#
# @pytest.mark.django_db
# def test_factions_2(create_admin):
#     faction = Faction.objects.first()
#     expected_result = "1 - Neutral"
#     assert expected_result == faction.__str__()
#     response = api_client.get("/api/v1/factions/")
#     assert response.status_code == HTTP_401_UNAUTHORIZED
#     admin = create_admin()
#     api_client.force_authenticate(admin)
#     response = api_client.get("/api/v1/factions/")
#     assert response.status_code == HTTP_200_OK
