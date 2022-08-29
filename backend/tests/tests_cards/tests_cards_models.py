import pytest

from apps.cards.models import Card, Deck, Leader


@pytest.mark.django_db
class TestCardsModels:
    def test_leader(self):
        """Проверка на наличие карты Лидера"""
        # Тест метода __str__ у модели, он должен показать то, как бы она print()
        leader = Leader.objects.first()
        expected_result = 'Foltest, ability 1 - damage-one, damage 2 charges 2'
        assert expected_result == leader.__str__()

    def test_cards(self):
        """Проверка на наличие карты с именем Tibor"""
        card = Card.objects.first()
        expected_result = 'Tibor'
        assert expected_result in card.__str__()

    def test_deck(self):
        """Проверка на наличие полей 'Bronze', 'Silver', 'Gold' и на длину строки"""
        deck = Deck.objects.first()
        expected_result = ['Bronze', 'Silver', 'Gold']
        for color in expected_result:
            assert color in deck.__str__()
        assert len(deck) == 2
