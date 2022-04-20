from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.accounts.models import CustomUser
from apps.cards.models import Card, Deck, Leader
from apps.cards.serializers import CardSerializer, DeckSerializer, LeaderSerializer, UserCardsSerializer


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
    queryset = Deck.objects.\
        select_related("leader__ability", "leader__faction").\
        prefetch_related("cards__type", "cards__color", "cards__ability", "cards__faction", "d").\
        all()
    serializer_class = DeckSerializer


class LeaderViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Leader.objects.select_related("ability", "faction").all()
    serializer_class = LeaderSerializer


class UserCardsViewSet(GenericViewSet, mixins.RetrieveModelMixin):

    queryset = CustomUser.objects.all()
    serializer_class = UserCardsSerializer
