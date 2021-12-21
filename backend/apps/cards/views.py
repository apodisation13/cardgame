from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ViewSet

from apps.cards.models import Card, Deck
from apps.cards.serializers import CardSerializer, DeckSerializer


class CardViewSet(ViewSet):
    def list(self, request):
        queryset = Card.objects.\
            select_related("faction").\
            select_related("color").\
            select_related("type").\
            select_related("ability").\
            all()
        serializer = CardSerializer(queryset, many=True)
        return Response(serializer.data)


class DeckViewSet(GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.DestroyModelMixin, ):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
