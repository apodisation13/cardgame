import pytest

from apps.core.models import Faction, Color, Type, Ability, Move, EnemyPassiveAbility, EnemyLeaderAbility

@pytest.mark.django_db
class TestModels:
    def test_factions(self):
        # Тест метода __str__ у модели, он должен показать то, как бы она print()
        faction = Faction.objects.first()
        expected_result = '1 - Neutral'
        # print(faction)
        assert expected_result == faction.__str__()

    def test_color(self):
        """Проверка цвета карт"""
        color = Color.objects.all()
        expected_result = ['Bronze', 'Silver', 'Gold']
        # print(color)
        for i in expected_result:
            assert i in color.__str__()

    def test_type(self):
        """Проверка типов карт"""
        type = Type.objects.all()
        expected_result = ['Unit', 'Special']
        # print(type)
        for i in expected_result:
            assert i in type.__str__()
        type = Type.objects.all()
        assert len(type) == 2

    def test_ability(self):
        """Проверка атрибутов карт"""
        ability = Ability.objects.first()
        expected_result = '1 - damage-one'
        # print(ability)
        assert expected_result == ability.__str__()

    def test_move(self):
        """Проверка способностей врагов ходить: down, stand, random"""
        move = Move.objects.all()
        expected_result = ['down', 'stand', 'random']
        # print(move)
        for i in expected_result:
            assert i in move.__str__()

    def test_enemy_passive_ability(self):
        """Проверка пассивных способностей врагов"""
        enemy_passive_ability = EnemyPassiveAbility.objects.first()
        expected_result = '1 - increase-damage'
        # print(enemy_passive_ability)
        assert expected_result == enemy_passive_ability.__str__()

    def test_enemy_leader_ability(self):
        """Проверка способностей лидеров врагов"""
        enemy_leader_ability = EnemyLeaderAbility.objects.first()
        expected_result = '1 - damage-once'
        # print(enemy_leader_ability)
        assert expected_result == enemy_leader_ability.__str__()




















