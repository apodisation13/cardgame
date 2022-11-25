import pytest
import rest_framework.status as status
from model_bakery import baker

from apps.cards.models import Card, CardDeck, Deck, Leader, UserCard, UserDeck, UserLeader

LOCKED_CARD = 1
UNLOCKED_CARD = 2
LOCKED_LEADER = 2
UNLOCKED_LEADER = 1
BASE_DECK = 1


@pytest.mark.django_db
class TestCardsAPI:
    @pytest.fixture
    def authenticated_user(self, api_client, create_user):
        user = create_user()
        api_client.force_authenticate(user=user)
        return user

    def test_mill_unlocked_card(self, api_client, authenticated_user):
        u_c = UserCard.objects.filter(user_id=authenticated_user.id).first()
        if u_c.count > 1:
            u_c.count = 1
            u_c.save()
        response = api_client.patch(
            f"/api/v1/patchcards/mill_user_cards/{u_c.id}/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST, 'Нельзя уничтожить карту из стартового набора'

    def test_mill_unlocked_leader(self, api_client, authenticated_user):
        u_l = UserLeader.objects.filter(user_id=authenticated_user.id).first()
        if u_l.count > 1:
            u_l.count = 1
            u_l.save()
        response = api_client.patch(
            f"/api/v1/patchleaders/mill_user_leaders/{u_l.id}/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST, 'Нельзя уничтожить лидера из стартового набора'

    def test_craft_locked_card(self, api_client, authenticated_user):
        data = {'user': authenticated_user.id, 'card': LOCKED_CARD, 'count': 1}
        url = '/api/v1/patchcards/craft_user_cards/'
        response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED, 'добавление карты'

        user_cards = response.data.get('cards')
        u_c_id = None
        for item in user_cards:
            if item['card']['id'] == data['card']:
                u_c_id = item['id']
                break
        assert u_c_id is not None, 'есть id записи в таблице UserCard'
        record = {'user': authenticated_user.id,
                  'card': item['card']['id'],
                  'count': item['count']}
        assert record == data, 'данные записаны правильно'

        response = api_client.patch(f"{url}{u_c_id}/")
        assert response.status_code == status.HTTP_200_OK, 'увеличение количества'

        user_cards = response.data.get('cards')
        count = None
        for item in user_cards:
            if item.get('id') == u_c_id:
                count = item['count']
                break
        assert count == data['count'] + 1, 'количество увеличилось'

    def test_craft_locked_leader(self, api_client, authenticated_user):
        data = {'user': authenticated_user.id, 'leader': LOCKED_LEADER,
                'count': 1}
        url = '/api/v1/patchleaders/craft_user_leaders/'
        response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED, 'добавление карты'

        user_leaders = response.data.get('leaders')
        u_l_id = None
        for item in user_leaders:
            if item['leader']['id'] == data['leader']:
                u_l_id = item['id']
                break
        assert u_l_id is not None, 'есть id записи в таблице UserLeader'
        record = {'user': authenticated_user.id,
                  'leader': item['leader']['id'],
                  'count': item['count']}
        assert record == data, 'данные записаны правильно'

        response = api_client.patch(f"{url}{u_l_id}/")
        assert response.status_code == status.HTTP_200_OK, 'увеличение количества'

        user_leaders = response.data.get('leaders')
        count = None
        for item in user_leaders:
            if item.get('id') == u_l_id:
                count = item['count']
                break
        assert count == data['count'] + 1, 'количество увеличилось'

    def test_mill_locked_card(self, api_client, authenticated_user):
        data = {'user': authenticated_user,
                'card': Card.objects.get(id=LOCKED_CARD), 'count': 2}
        u_c = UserCard.objects.create(**data)
        url = f"/api/v1/patchcards/mill_user_cards/{u_c.id}/"

        response = api_client.patch(url)
        assert response.status_code == status.HTTP_200_OK, 'уменьшение количества'

        user_cards = response.data.get('cards')
        count = None
        for item in user_cards:
            if item.get('id') == u_c.id:
                count = item['count']
                break
        assert count == data['count'] - 1, 'количество уменьшилось'

        response = api_client.patch(url)
        assert response.status_code == status.HTTP_200_OK, 'уменьшение количества до нуля'

        user_cards = response.data.get('cards')
        count = None
        for item in user_cards:
            if item.get('id') == u_c.id:
                count = item['count']
                break
        assert count is None, 'запись удалена'

    def test_mill_locked_leader(self, api_client, authenticated_user):
        data = {'user': authenticated_user,
                'leader': Leader.objects.get(id=LOCKED_LEADER), 'count': 2}
        u_l = UserLeader.objects.create(**data)
        url = f'/api/v1/patchleaders/mill_user_leaders/{u_l.id}/'

        response = api_client.patch(url)
        assert response.status_code == status.HTTP_200_OK, 'уменьшение количества'

        user_leaders = response.data.get('leaders')
        count = None
        for item in user_leaders:
            if item.get('id') == u_l.id:
                count = item['count']
                break
        assert count == data['count'] - 1, 'количество уменьшилось'

        response = api_client.patch(url)
        assert response.status_code == status.HTTP_200_OK, 'уменьшение количества до нуля'

        user_leaders = response.data.get('leaders')
        count = None
        for item in user_leaders:
            if item.get('id') == u_l.id:
                count = item['count']
                break
        assert count is None, 'запись удалена'

    @pytest.fixture
    def deck_factory(self):
        def factory(*args, **kwargs):
            return baker.make(Deck, *args, **kwargs)
        return factory

    def test_create_deck(self, api_client, authenticated_user):
        decks_count = UserDeck.objects.filter(user__id=authenticated_user.id).count()
        url = "/api/v1/decks/"
        data = {'name': 'test deck', 'd': [{'card': UNLOCKED_CARD}],
                'leader_id': UNLOCKED_LEADER}

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED, 'создание колоды'
        assert len(response.data) == decks_count + 1, 'количество колод юзера увеличилось'

    def test_update_deck(self, api_client, authenticated_user, create_user, deck_factory):
        u_d = UserDeck.objects.create(user=authenticated_user, deck=deck_factory())
        deck_id = u_d.deck.id
        deck_length = CardDeck.objects.filter(deck__id=deck_id).count()
        url = f"/api/v1/decks/{deck_id}/"
        data = {'name': 'test deck',
                'd': [{'card': i} for i in range(1, deck_length + 1)],
                'leader_id': UNLOCKED_LEADER}

        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_200_OK, 'изменение своей колоды'

        other_user = create_user()
        api_client.force_authenticate(other_user)

        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_404_NOT_FOUND, 'изменение чужой колоды'

    def test_delete_deck(self, api_client, authenticated_user, create_user, deck_factory):
        u_d = UserDeck.objects.create(user=authenticated_user, deck=deck_factory())
        deck_id = u_d.deck.id
        url = f"/api/v1/decks/{deck_id}/"

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_200_OK, 'удаление своей колоды'

        other_user = create_user()
        api_client.force_authenticate(other_user)

        response = api_client.patch(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND, 'удаление чужой колоды'

    def test_change_base_deck(self, api_client, authenticated_user):
        url = f"/api/v1/decks/{BASE_DECK}/"

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_403_FORBIDDEN, 'удаление базовой колоды'

        deck_length = CardDeck.objects.filter(deck__id=BASE_DECK).count()
        data = {'name': 'test deck',
                'd': [{'card': i} for i in range(1, deck_length + 1)],
                'leader_id': UNLOCKED_LEADER}

        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, 'изменение базовой колоды'
