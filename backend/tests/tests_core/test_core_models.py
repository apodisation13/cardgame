import pytest

from apps.core.models import Ability, Color, Faction, Type


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
