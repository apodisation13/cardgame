import pytest

from apps.enemies.models import Enemy, EnemyLeader


@pytest.mark.django_db
class TestModels:
    def test_enemy(self):
        enemy = Enemy.objects.first()
        expected_result = ['Soldiers', 'Bronze']
        for data in expected_result:
            assert data in enemy.__str__()

    def test_enemyleader(self):
        enemyleader = EnemyLeader.objects.all()
        expected_result = ['First Enemy Leader', 'Second Enemy Leader']
        for data in expected_result:
            assert data in enemyleader.__str__()
