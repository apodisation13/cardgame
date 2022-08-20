import pytest
from rest_framework.test import APIClient
from rest_framework.status import HTTP_401_UNAUTHORIZED, HTTP_200_OK

from apps.core.models import Faction


# @pytest.mark.django_db(transaction=True, reset_sequences=True)
@pytest.mark.django_db
class TestModels:
    def setup(self):
        self.api_client = APIClient()

    def test_factions(self, load_database):
        faction = Faction.objects.first()
        expected_result = "1 - Neutral"
        assert expected_result == faction.__str__()

    def test_faction_api(self, create_admin):
        faction = Faction.objects.first()
        print(faction)
        response = self.api_client.get("/api/v1/factions/")
        assert response.status_code == HTTP_401_UNAUTHORIZED
        admin = create_admin()
        self.api_client.force_authenticate(admin)
        response = self.api_client.get("/api/v1/factions/")
        assert response.status_code == HTTP_200_OK
