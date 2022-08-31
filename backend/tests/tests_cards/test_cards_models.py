import pytest

from apps.cards.models import Card, Deck, Leader


@pytest.mark.django_db
class TestCardsModels:
    def test_leader(self):
        """Проверка на наличие карты Лидера"""
        leader = Leader.objects.first()
        expected_result = 'Foltest, ability 1 - damage-one, damage 2 charges 2'
        assert expected_result == leader.__str__()

    def test_cards(self):
        """Проверка на наличие карты с именем Tibor"""
        card = Card.objects.first()
        expected_result = 'Tibor'
        assert expected_result in card.__str__()

    def test_deck(self):
        """Проверка на наличие поля"""
        decks = Deck.objects.all()
        assert decks[0].__str__() == '1, name base-deck, health 70, Foltest, ability 1 - damage-one, damage 2 charges 2'
        assert len(decks) == 1
