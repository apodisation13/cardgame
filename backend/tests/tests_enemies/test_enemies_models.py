import pytest

from apps.enemies.models import Enemy, EnemyLeader, Level


@pytest.mark.django_db
class TestModels:
    def test_enemy(self):
        enemy = Enemy.objects.first()
        expected_result = ['Soldiers', 'Bronze']
        for i in expected_result:
            assert i in enemy.__str__()
        enemy_all = Enemy.objects.all()
        assert len(enemy_all) == 43

    def test_enemyleader(self):
        enemyleader = EnemyLeader.objects.all()
        expected_result = ['First Enemy Leader', 'Second Enemy Leader']
        for i in expected_result:
            assert i in enemyleader.__str__()

    def test_level(self):
        level = Level.objects.all()
        assert level.__str__()
