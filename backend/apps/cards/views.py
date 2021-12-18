from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, GenericViewSet

from apps.cards.models import Card, Try, Deck
from apps.cards.serializers import CardSerializer, TrySerializer, DeckSerializer


class CardViewSet(ViewSet):
    def list(self, request):
        queryset = Card.objects.\
            select_related("faction").\
            select_related("color").\
            select_related("type").\
            select_related("ability").\
            order_by("-hp").\
            all()
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)


class TryViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = Try.objects.all()
    serializer_class = TrySerializer


class DeckViewSet(GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
