from rest_framework import mixins
# from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
# from rest_framework.views import Response

from apps.cards.models import Card, Deck, Leader, UserCard
from apps.cards.serializers import CardSerializer, DeckSerializer, LeaderSerializer, CraftUserCardSerializer, \
    MillUserCardSerializer


class CardViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Card.objects.select_related("faction", "color", "type", "ability").all()
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
        select_related("leader__ability", "leader__faction"). \
        prefetch_related("cards__type", "cards__color", "cards__ability", "cards__faction", "d"). \
        all()
    serializer_class = DeckSerializer


class LeaderViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Leader.objects.select_related("ability", "faction").all()
    serializer_class = LeaderSerializer


class CraftUserCardViewSet(GenericViewSet,
                           # mixins.ListModelMixin,
                           mixins.CreateModelMixin,
                           # mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           ):
    queryset = UserCard.objects.all()
    serializer_class = CraftUserCardSerializer
    http_method_names = ["patch", "post"]  # убрать метод PUT, который не нужен

    # @action(methods=["get", "patch"], detail=True)
    # def usercards(self, request, pk=None):
    #     usercards = self.queryset.filter(user_id=pk).all()
    #     serializer = self.serializer_class(usercards, many=True)
    #     return Response(serializer.data)


class MillUserCardViewSet(GenericViewSet,
                          mixins.UpdateModelMixin
                          ):
    queryset = UserCard.objects.all()
    serializer_class = MillUserCardSerializer
    http_method_names = ["patch"]
