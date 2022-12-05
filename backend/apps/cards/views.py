from rest_framework import mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.cards.mixins import CardBaseMixin, DeckBaseMixin, LeaderBaseMixin
from apps.cards.models import Card, Deck, Leader, UserCard, UserDeck, UserLeader
from apps.cards.serializers import (
    CardSerializer,
    CraftUserCardSerializer,
    CraftUserLeaderSerializer,
    DeckSerializer,
    LeaderSerializer,
    MillUserCardSerializer,
    MillUserLeaderSerializer,
    UserDeckSerializer,
)
from apps.user_database.serializers import UserDecksThroughSerializer
from apps.user_database.utils import get_cards_for_user


class CardViewSet(GenericViewSet,
                  mixins.ListModelMixin
                  ):
    queryset = Card.objects.select_related("faction", "color", "type", "ability", "passive_ability").all()
    serializer_class = CardSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class LeaderViewSet(GenericViewSet,
                    mixins.ListModelMixin
                    ):
    queryset = Leader.objects.select_related("ability", "faction", "passive_ability").all()
    serializer_class = LeaderSerializer

    def get_serializer_context(self):
        return {'request': self.request}


class DeckViewSet(DeckBaseMixin,
                  GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  ):

    serializer_class = DeckSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        return Deck.objects.filter(u_d__user_id=self.request.user.id). \
            select_related("leader__ability", "leader__faction",
                           "leader__passive_ability"). \
            prefetch_related("cards__type", "cards__color", "cards__ability",
                             "cards__faction", "cards__passive_ability", "d"). \
            all()

    def get_serializer_context(self):
        return {'request': self.request}

    def return_all_decks(self, status_code=status.HTTP_200_OK):
        u_d = UserDeck.objects.filter(user_id=self.request.user.id).all()
        serializer = UserDecksThroughSerializer(u_d, context=self.get_serializer_context(), many=True)
        return Response(serializer.data, status=status_code)

    def is_base_deck(self):
        return int(self.kwargs.get('pk')) == 1

    def list(self, request, *args, **kwargs):
        return self.return_all_decks()

    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return self.return_all_decks(status_code=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        if self.is_base_deck():
            return Response({'error': 'Cannot delete base deck'}, status=status.HTTP_403_FORBIDDEN)
        super().destroy(request, *args, **kwargs)
        return self.return_all_decks()

    def update(self, request, *args, **kwargs):
        if self.is_base_deck():
            return Response({'error': 'Cannot change base deck'}, status=status.HTTP_403_FORBIDDEN)
        super().update(request, *args, **kwargs)
        return self.return_all_decks()


class CraftUserCardViewSet(CardBaseMixin,
                           GenericViewSet,
                           # mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           ):
    """GET - просмотр всех карт,

    POST - добавление юзеру списка карт cards (если нет - создаётся запись в UserCard, если есть - +1),

    PATCH - увеличение количества на 1 (данные в запросе не нужны).

    Все методы возвращают все карты. Для карт юзера дополнительно
    возвращется их количество и id записи в UserCard. Для для остальных count=0.
    """
    queryset = UserCard.objects.all()
    serializer_class = CraftUserCardSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "post", "patch"]  # убрать метод PUT, который не нужен

    def list(self, request, *args, status=status.HTTP_200_OK, **kwargs):
        cards = get_cards_for_user(request, request.user.id, CardSerializer)
        return Response({'cards': cards}, status=status)

    def create(self, request, *args, **kwargs):
        cards = request.data.get('cards')
        if not cards:
            return Response(data={'error': "No cards for craft. "
                                           "Request body should contain 'cards': a list of card ids."},
                            status=status.HTTP_400_BAD_REQUEST)
        u_c = self.queryset.filter(user_id=request.user.id)
        card__user_card_mapping = {obj.card_id: obj.id for obj in u_c}
        for card in cards:
            if card not in card__user_card_mapping.keys():
                request.data.update(card=card)
                super().create(request, *args, **kwargs)
            else:
                self.kwargs.update(pk=card__user_card_mapping[card])
                request.data.pop('card', None)
                super().update(request, *args, partial=True, **kwargs)
        self.kwargs.pop('pk', None)
        request.data.pop('card', None)
        return self.list(request, *args, status=status.HTTP_201_CREATED, **kwargs)

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)


class MillUserCardViewSet(CardBaseMixin,
                          GenericViewSet,
                          mixins.UpdateModelMixin
                          ):
    """Уменьшение количества карты юзера на 1.
    Возвращает все карты.
    Никакие данные в запросе не нужны (кроме id в адресе).
    При уменьшении до 0 запись удаляется.
    """
    queryset = UserCard.objects.all()
    serializer_class = MillUserCardSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["patch"]


class CraftUserLeaderViewSet(LeaderBaseMixin,
                             GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             ):
    """Просмотр всех лидеров юзера, добавление лидера или увеличение его количества на 1.
    Возвращает всех лидеров юзера.
    Для увеличения количества никакие данные в запросе не нужны (кроме id в адресе).
    """
    queryset = UserLeader.objects.all()
    serializer_class = CraftUserLeaderSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "post", "patch"]  # убрать метод PUT, который не нужен


class MillUserLeaderViewSet(LeaderBaseMixin,
                            GenericViewSet,
                            mixins.UpdateModelMixin
                            ):
    """Уменьшение количества карты лидера у юзера на 1.
    Возвращает всех лидеров юзера.
    Никакие данные в запросе не нужны (кроме id в адресе).
    При уменьшении до 0 запись удаляется.
    """
    queryset = UserLeader.objects.all()
    serializer_class = MillUserLeaderSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["patch"]


class UserDeckViewSet(DeckBaseMixin,
                      GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin
                      ):
    queryset = UserDeck.objects.all()
    serializer_class = UserDeckSerializer
    authentication_classes = [TokenAuthentication]
