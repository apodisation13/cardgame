import pytest

from apps.enemies.models import Enemy, EnemyLeader, Level

@pytest.mark.django_db
class TestModels:
    def test_enemy(self):
        enemy = Enemy.objects.first()
        expected_result = ['Soldiers', 'Bronze']
        # print(enemy)
        for i in expected_result:
            assert i in enemy.__str__()
        enemy = Enemy.objects.all()
        assert len(enemy) == 43

    def test_enemyleader(self):
        enemyleader = EnemyLeader.objects.all()
        expected_result = ['First Enemy Leader', 'Second Enemy Leader']
        # print(enemyleader)
        for i in expected_result:
            assert i in enemyleader.__str__()

    def test_level(self):
        level = Level.objects.all()
        # print(level)

