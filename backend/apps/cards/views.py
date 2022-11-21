from rest_framework import mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.settings import api_settings
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
                  ):

    serializer_class = DeckSerializer
    authentication_classes = [TokenAuthentication]
    http_method_names = ["get", "post", "patch", "delete"]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_queryset(self):
        return Deck.objects.filter(u_d__user_id=self.request.user.id). \
            select_related("leader__ability", "leader__faction",
                           "leader__passive_ability"). \
            prefetch_related("cards__type", "cards__color", "cards__ability",
                             "cards__faction", "cards__passive_ability", "d"). \
            all()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    def get_success_headers(self, data):
        try:
            return {'Location': str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        instance.delete()

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        return Response(serializer.data)

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)


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
