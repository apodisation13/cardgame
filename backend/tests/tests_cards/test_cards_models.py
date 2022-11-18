import pytest
from rest_framework.test import APIClient

from apps.accounts.models import CustomUser
from apps.cards.models import Card, Deck, Leader

LOCKED_CARD = 1
UNLOCKED_CARD = 2
LOCKED_LEADER = 2
UNLOCKED_LEADER = 1


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


@pytest.mark.django_db
class TestCardAPI:
    @pytest.fixture
    def api_client(self):
        return APIClient()

    @pytest.fixture
    def auth_user(self, api_client):
        user = CustomUser.objects.create_user('test_user')
        api_client.force_authenticate(user=user)
        return user

    test_data_mill_unlocked_card = [
        ['/api/v1/patchcards/mill_user_cards/1/', 400, 'Нельзя уничтожить карту из стартового набора'],
        ['/api/v1/patchleaders/mill_user_leaders/1/', 400, 'Нельзя уничтожить лидера из стартового набора'],
    ]

    @pytest.mark.parametrize('url, expected_status, description',
                             test_data_mill_unlocked_card)
    def test_mill_unlocked_card(self, api_client, auth_user,
                                url, expected_status, description):
        response = api_client.patch(url)
        assert response.status_code == expected_status, description

    def test_craft_mill_locked_card(self, api_client, auth_user):
        data = {'user': auth_user.id, 'card': LOCKED_CARD, 'count': 1}
        response = api_client.post('/api/v1/patchcards/craft_user_cards/',
                                   data=data)
        assert response.status_code == 201, 'добавление карты'

        user_cards = response.data.get('cards')
        u_c_id = None
        for item in user_cards:
            if item['card']['id'] == LOCKED_CARD:
                u_c_id = item['id']
                break
        assert u_c_id is not None, 'есть id записи в таблице UserCard'

        response = api_client.patch(f"/api/v1/patchcards/craft_user_cards/{u_c_id}/")
        assert response.status_code == 200, 'увеличение количества'

        user_cards = response.data.get('cards')
        count = None
        for item in user_cards:
            if item.get('id') == u_c_id:
                count = item['count']
                break
        assert count == data['count'] + 1, 'количество увеличилось'

        response = api_client.patch(f"/api/v1/patchcards/mill_user_cards/{u_c_id}/")
        assert response.status_code == 200, 'уменьшение количества'

        user_cards = response.data.get('cards')
        count = None
        for item in user_cards:
            if item.get('id') == u_c_id:
                count = item['count']
                break
        assert count == data['count'], 'количество уменьшилось'

        response = api_client.patch(f"/api/v1/patchcards/mill_user_cards/{u_c_id}/")
        assert response.status_code == 200, 'уменьшение количества до нуля'

        user_cards = response.data.get('cards')
        count = None
        for item in user_cards:
            if item.get('id') == u_c_id:
                count = item['count']
                break
        assert count is None, 'запись удалена'
