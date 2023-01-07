import pytest
import rest_framework.status as status
from django.db.models import F
from django.urls import reverse
from model_bakery import baker

from apps.cards.models import Card, Deck, Leader, UserCard, UserDeck, UserLeader
from apps.core.models import GameConst

LOCKED_CARD = 1  # id карты НЕ из стартового набора
UNLOCKED_CARD = 2  # id карты из стартового набора
LOCKED_LEADER = 2  # id лидера НЕ из стартового набора
UNLOCKED_LEADER = 1  # id лидера из стартового набора
BASE_DECK = 1  # id базовой колоды
INITIAL_COUNT = 1  # Количество карты при создании
TEST_DECK = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]  # Колода для тестирования
GOLD_CARD = 2  # id золотой карты из стартового набора
SILVER_CARD = 8  # id серебряной карты из стартового набора
BRONZE_CARD = 3  # id бронзовой карты из стартового набора


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
        data = {'user': authenticated_user.id, 'card': LOCKED_CARD}
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
        assert record == {**data, 'count': INITIAL_COUNT}, 'данные записаны правильно'

        response = api_client.patch(f"{url}{u_c_id}/")
        assert response.status_code == status.HTTP_200_OK, 'увеличение количества'

        user_cards = response.data.get('cards')
        count = None
        for item in user_cards:
            if item.get('id') == u_c_id:
                count = item['count']
                break
        assert count == INITIAL_COUNT + 1, 'количество увеличилось'

    def test_craft_locked_leader(self, api_client, authenticated_user):
        data = {'user': authenticated_user.id, 'leader': LOCKED_LEADER}
        url = '/api/v1/patchleaders/craft_user_leaders/'
        response = api_client.post(url, data=data)
        assert response.status_code == status.HTTP_201_CREATED, 'добавление карты'

        user_leaders = response.data.get('leaders')
        u_l_id = None
        for item in user_leaders:
            if item['card']['id'] == data['leader']:
                u_l_id = item['id']
                break
        assert u_l_id is not None, 'есть id записи в таблице UserLeader'
        record = {'user': authenticated_user.id,
                  'leader': item['card']['id'],
                  'count': item['count']}
        assert record == {**data, 'count': INITIAL_COUNT}, 'данные записаны правильно'

        response = api_client.patch(f"{url}{u_l_id}/")
        assert response.status_code == status.HTTP_200_OK, 'увеличение количества'

        user_leaders = response.data.get('leaders')
        count = None
        for item in user_leaders:
            if item.get('id') == u_l_id:
                count = item['count']
                break
        assert count == INITIAL_COUNT + 1, 'количество увеличилось'

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

    @pytest.mark.parametrize(
        'url, card, description',
        [('/api/v1/patchcards/craft_user_cards/', LOCKED_CARD, 'создание карты другому юзеру'),
         ('/api/v1/patchleaders/craft_user_leaders/', LOCKED_LEADER, 'создание лидера другому юзеру')])
    def test_create_card_for_other_user(self, api_client, authenticated_user, create_user,
                                        url, card, description):
        data = {'user': authenticated_user.id, 'card': card}
        other_user = create_user()
        api_client.force_authenticate(other_user)

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, description

    @pytest.mark.parametrize(
        'url, model, description',
        [('/api/v1/patchcards/craft_user_cards/', 'UserCard', 'изменение чужой карты'),
         ('/api/v1/patchleaders/craft_user_leaders/', 'UserLeader', 'изменение чужого лидера'),
         ('/api/v1/patchcards/mill_user_cards/', 'UserCard', 'удаление чужой карты'),
         ('/api/v1/patchleaders/mill_user_leaders/', 'UserLeader', 'удаление чужого лидера')]
    )
    def test_craft_mill_other_user_card(self, api_client, authenticated_user,
                                        create_user, url, model, description):
        model = eval(f'{model}')
        record_id = model.objects.filter(user_id=authenticated_user.id).first().id
        other_user = create_user()
        api_client.force_authenticate(other_user)

        response = api_client.patch(f"{url}/{record_id}/")

        assert response.status_code == status.HTTP_404_NOT_FOUND, description

    @pytest.fixture
    def deck_factory(self):
        def factory(*args, **kwargs):
            return baker.make(Deck, *args, **kwargs)
        return factory

    def test_create_deck(self, api_client, authenticated_user):
        decks_count = UserDeck.objects.filter(user__id=authenticated_user.id).count()
        url = "/api/v1/decks/"
        data = {'name': 'test deck', 'd': [{'card': i} for i in TEST_DECK],
                'leader_id': UNLOCKED_LEADER}

        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED, 'создание колоды'
        assert len(response.data) == decks_count + 1, 'количество колод юзера увеличилось'

    def test_update_deck(self, api_client, authenticated_user, create_user, deck_factory):
        u_d = UserDeck.objects.create(user=authenticated_user, deck=deck_factory())
        deck_id = u_d.deck.id
        url = f"/api/v1/decks/{deck_id}/"
        data = {'name': 'test deck',
                'd': [{'card': i} for i in TEST_DECK],
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

        data = {'name': 'test deck',
                'd': [{'card': i} for i in TEST_DECK],
                'leader_id': UNLOCKED_LEADER}

        response = api_client.patch(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN, 'изменение базовой колоды'

    def test_mega_mill(self, api_client, authenticated_user):
        url = reverse('mega-mill')
        user_cards = UserCard.objects.filter(user_id=authenticated_user.id)
        user_cards.filter(
            card__in=[BRONZE_CARD, SILVER_CARD, GOLD_CARD]
        ).update(count=F('count') + 1)
        initial_scraps = authenticated_user.scraps
        game_const = GameConst.objects.first().data
        scraps_to_add = sum(
            game_const[item]
            for item in ['mill_gold', 'mill_silver', 'mill_bronze']
        )

        response = api_client.post(url)

        assert response.status_code == status.HTTP_200_OK, 'Mega Mill'
        assert response.data['scraps'] == initial_scraps + scraps_to_add, 'Добавление ресурсов'
        for card in response.data['cards']:
            assert card['count'] <= 1, 'Количество каждой карты не больше 1'
