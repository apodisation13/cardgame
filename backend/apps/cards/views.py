from rest_framework import mixins
# from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.cards.permissions import IsOwner
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


class BaseMixin:
    def get_permissions(self):
        """get - только админ, post,patch - только тот юзер, который там в теле запроса"""
        if self.action in ["create", "partial_update"]:
            return [IsOwner()]
        elif self.action == "list":
            return [IsAdminUser()]
        return []


class CardViewSet(GenericViewSet,
                  mixins.ListModelMixin
                  ):
    queryset = Card.objects.select_related("faction", "color", "type", "ability", "passive_ability").all()
    serializer_class = CardSerializer

    # # ВОТ ТАК ТУДА МОЖНО ПЕРЕДАТЬ ПАРАМЕТР request, self.context['request']
    # def get_serializer_context(self):
    #     return {'request': self.request}


class DeckViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin,
                  mixins.UpdateModelMixin,
                  ):
    queryset = Deck.objects. \
        select_related("leader__ability", "leader__faction", "leader__passive_ability"). \
        prefetch_related("cards__type", "cards__color", "cards__ability",
                         "cards__faction", "cards__passive_ability", "d"). \
        all()
    serializer_class = DeckSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


class LeaderViewSet(GenericViewSet,
                    mixins.ListModelMixin
                    ):
    queryset = Leader.objects.select_related("ability", "faction", "passive_ability").all()
    serializer_class = LeaderSerializer


class CraftUserCardViewSet(BaseMixin,
                           GenericViewSet,
                           mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           mixins.UpdateModelMixin,
                           ):
    queryset = UserCard.objects.all()
    serializer_class = CraftUserCardSerializer
    http_method_names = ["patch", "post", "get"]  # убрать метод PUT, который не нужен
    authentication_classes = [TokenAuthentication]

    # @action(methods=["get", "patch"], detail=True)
    # def usercards(self, request, pk=None):
    # from rest_framework.views import Response
    #     usercards = self.queryset.filter(user_id=pk).all()
    #     serializer = self.serializer_class(usercards, many=True)
    #     return Response(serializer.data)


class MillUserCardViewSet(BaseMixin,
                          GenericViewSet,
                          mixins.UpdateModelMixin
                          ):
    queryset = UserCard.objects.all()
    serializer_class = MillUserCardSerializer
    http_method_names = ["patch"]
    authentication_classes = [TokenAuthentication]


class CraftUserLeaderViewSet(BaseMixin,
                             GenericViewSet,
                             mixins.ListModelMixin,
                             mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             ):
    queryset = UserLeader.objects.all()
    serializer_class = CraftUserLeaderSerializer
    http_method_names = ["patch", "post", "get"]  # убрать метод PUT, который не нужен
    authentication_classes = [TokenAuthentication]


class MillUserLeaderViewSet(BaseMixin,
                            GenericViewSet,
                            mixins.UpdateModelMixin
                            ):
    queryset = UserLeader.objects.all()
    serializer_class = MillUserLeaderSerializer
    http_method_names = ["patch"]
    authentication_classes = [TokenAuthentication]


class UserDeckViewSet(BaseMixin,
                      GenericViewSet,
                      mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin
                      ):
    queryset = UserDeck.objects.all()
    # serializer_class = UserDecksThroughSerializer
    serializer_class = UserDeckSerializer
    authentication_classes = [TokenAuthentication]
