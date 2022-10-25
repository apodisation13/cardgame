from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from apps.enemies.models import Enemy, EnemyLeader, Level, UserLevel, Season
from apps.enemies.serializers import EnemyLeaderSerializer, EnemySerializer, LevelSerializer, UnlockLevelsSerializer, \
    SeasonSerializer


class EnemyViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Enemy.objects.select_related("faction", "color", "move", "passive_ability").all()
    serializer_class = EnemySerializer
    permission_classes = [IsAuthenticated]


class EnemyLeaderViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = EnemyLeader.objects.select_related("faction", "ability").all()
    serializer_class = EnemyLeaderSerializer
    permission_classes = [IsAuthenticated]


class LevelViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Level.objects.\
        select_related("enemy_leader__ability", "enemy_leader__faction").\
        prefetch_related("enemies__faction", "enemies__color", "enemies__move", "enemies__passive_ability").\
        all()
    serializer_class = LevelSerializer


class UnlockLevelsViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.UpdateModelMixin):
    queryset = UserLevel.objects.all()
    serializer_class = UnlockLevelsSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]  # TODO: здесь должно быть isObjectOwner, ну типа только себе может открывать


class SeasonViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Season.objects.all()
    serializer_class = SeasonSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
