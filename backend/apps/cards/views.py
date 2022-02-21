from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.cards.models import Card, Deck, Faction, Leader
from apps.cards.serializers import CardSerializer, DeckSerializer, FactionSerializer, LeaderSerializer


class CardViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Card.objects.select_related("faction", "color", "type", "ability").all()
    serializer_class = CardSerializer


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


class FactionViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Faction.objects.all()
    serializer_class = FactionSerializer


class LeaderViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Leader.objects.select_related("ability", "faction").all()
    serializer_class = LeaderSerializer
