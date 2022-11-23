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
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status_code)

    def is_base_deck(self):
        return self.kwargs.get('pk') == 1

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
    queryset = UserCard.objects.all()
    serializer_class = CraftUserCardSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "post", "patch"]  # убрать метод PUT, который не нужен


class MillUserCardViewSet(CardBaseMixin,
                          GenericViewSet,
                          mixins.UpdateModelMixin
                          ):
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
    queryset = UserLeader.objects.all()
    serializer_class = CraftUserLeaderSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "post", "patch"]  # убрать метод PUT, который не нужен


class MillUserLeaderViewSet(LeaderBaseMixin,
                            GenericViewSet,
                            mixins.UpdateModelMixin
                            ):
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
