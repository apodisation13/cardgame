from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.enemies.models import Enemy, Level
from apps.enemies.serializers import EnemySerializer, LevelSerializer


class EnemyViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Enemy.objects.select_related('faction', 'color', 'move').all()
    serializer_class = EnemySerializer


class LevelViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Level.objects.prefetch_related("enemies__faction", "enemies__color", "enemies__move").all()
    serializer_class = LevelSerializer
