import pytest
from apps.core.models import (Ability, Color, EnemyLeaderAbility,
                              EnemyPassiveAbility, Faction, Move,
                              PassiveAbility, Type)


@pytest.mark.django_db
class TestModels:
    def test_factions(self):
        """Проверка фракций"""
        # Тест метода __str__ у модели, он должен показать то, как бы она print()
        faction = Faction.objects.all()
        expected_result = '1 - Neutral'
        assert expected_result[0] in faction.__str__()
        assert len(faction) == 4

    def test_color(self):
        """Проверка цвета карт"""
        colors = Color.objects.all()
        expected_result = ['Bronze', 'Silver', 'Gold']
        data_color = '1 - Bronze'
        for color in expected_result:
            assert color in colors.__str__()
        assert data_color == colors[0].__str__()

    def test_type(self):
        """Проверка типов карт"""
        type_all = Type.objects.all()
        expected_result = ['Unit', 'Special']
        for type_card in expected_result:
            assert type_card in type_all.__str__()
        assert len(type_all) == 2

    def test_ability(self):
        """Проверка атрибутов карт"""
        ability = Ability.objects.first()
        expected_result = '1 - damage-one'
        assert expected_result == ability.__str__()

    def test_passive_ability(self):
        """Проверка passive_ability"""
        passive_ability = PassiveAbility.objects.first()
        expected_result = '1 - add-charges-to-leader-if-play-special'
        assert expected_result == passive_ability.__str__()

    def test_move(self):
        """Проверка способностей врагов ходить: down, stand, random"""
        move = Move.objects.all()
        expected_result = ['down', 'stand', 'random']
        for ability in expected_result:
            assert ability in move.__str__()

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
