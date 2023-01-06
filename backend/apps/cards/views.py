from django.db.models import F
from rest_framework import mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.accounts.models import CustomUser
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
from apps.cards.utils import get_cards_to_mill
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
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           ):
    """Просмотр всех карт юзера, добавление карты или увеличение её количества на 1.
    Возвращает все карты юзера.
    Для увеличения количества никакие данные в запросе не нужны (кроме id в адресе).
    """
    queryset = UserCard.objects.all()
    serializer_class = CraftUserCardSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "post", "patch"]  # убрать метод PUT, который не нужен


class MillUserCardViewSet(CardBaseMixin,
                          GenericViewSet,
                          mixins.UpdateModelMixin
                          ):
    """Уменьшение количества карты юзера на 1.
    Возвращает все карты юзера.
    Никакие данные в запросе не нужны (кроме id в адресе).
    При уменьшении до 0 запись удаляется.
    """
    queryset = UserCard.objects.all()
    serializer_class = MillUserCardSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["patch"]


class MegaMillCardView(APIView):
    """Mega Mill - оставляет всех карт по одной,
    остальные уничтожает, возвращая часть ресурсов
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post']

    def get(self, request):
        """Считает, сколько карт будет уничтожено и сколько ресурсов получено"""
        user_cards = UserCard.objects.filter(user_id=request.user.id)
        cards_to_mill = get_cards_to_mill(user_cards)
        return Response(cards_to_mill)

    def post(self, request):
        """Оставляет всех карт по одной, остальные уничтожает.
        Возвращает карты и ресурсы в обновлённом количестве.
        """
        user_cards = UserCard.objects.filter(user_id=request.user.id)
        cards_to_mill = get_cards_to_mill(user_cards)
        total_for_mill = sum(item['mill_count'] * item['scraps_for_card']
                             for item in cards_to_mill)

        user_cards.update(count=1)
        user = CustomUser.objects.get(id=request.user.id)
        user.scraps = F('scraps') + total_for_mill
        user.save()
        user.refresh_from_db()

        return Response({
            "cards": get_cards_for_user(request=request,
                                        user_id=request.user.id,
                                        card_serializer=CardSerializer),
            "scraps": user.scraps
        })


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
