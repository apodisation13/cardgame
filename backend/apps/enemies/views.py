from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.enemies.models import Enemy, EnemyLeader, Level
from apps.enemies.serializers import EnemyLeaderSerializer, EnemySerializer, LevelSerializer


class EnemyViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Enemy.objects.select_related("faction", "color", "move", "passive_ability").all()
    serializer_class = EnemySerializer


class LevelViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Level.objects.\
        select_related("enemy_leader__ability", "enemy_leader__faction").\
        prefetch_related("enemies__faction", "enemies__color", "enemies__move", "enemies__passive_ability").\
        all()
    serializer_class = LevelSerializer


class EnemyLeaderViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = EnemyLeader.objects.select_related("faction", "ability").all()
    serializer_class = EnemyLeaderSerializer
