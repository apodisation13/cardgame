import pytest

from apps.core.models import Ability, Color, EnemyLeaderAbility, EnemyPassiveAbility, Faction, Move, Type


@pytest.mark.django_db
class TestModels:
    def test_factions(self):
        # Тест метода __str__ у модели, он должен показать то, как бы она print()
        faction = Faction.objects.first()
        expected_result = '1 - Neutral'
        assert expected_result in faction.__str__()
        faction_all = Faction.objects.all()
        assert len(faction_all) == 4

    def test_color(self):
        """Проверка цвета карт"""
        color = Color.objects.all()
        expected_result = ['Bronze', 'Silver', 'Gold']
        for i in expected_result:
            assert i in color.__str__()

    def test_type(self):
        """Проверка типов карт"""
        type_all = Type.objects.all()
        expected_result = ['Unit', 'Special']
        for i in expected_result:
            assert i in type_all.__str__()
        assert len(type_all) == 2

    def test_ability(self):
        """Проверка атрибутов карт"""
        ability = Ability.objects.first()
        expected_result = '1 - damage-one'
        assert expected_result == ability.__str__()

    def test_move(self):
        """Проверка способностей врагов ходить: down, stand, random"""
        move = Move.objects.all()
        expected_result = ['down', 'stand', 'random']
        for i in expected_result:
            assert i in move.__str__()

    def test_enemy_passive_ability(self):
        """Проверка пассивных способностей врагов"""
        enemy_passive_ability = EnemyPassiveAbility.objects.first()
        expected_result = '1 - increase-damage'
        assert expected_result == enemy_passive_ability.__str__()

    def test_enemy_leader_ability(self):
        """Проверка способностей лидеров врагов"""
        enemy_leader_ability = EnemyLeaderAbility.objects.first()
        expected_result = '1 - damage-once'
        assert expected_result == enemy_leader_ability.__str__()
