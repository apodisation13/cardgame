from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.enemies.models import Enemy, EnemyLeader, Level
from apps.enemies.serializers import EnemyLeaderSerializer, EnemySerializer, LevelSerializer, RelatedLevelSerializer
from apps.accounts.models import CustomUser


class EnemyViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Enemy.objects.select_related("faction", "color", "move", "passive_ability").all()
    serializer_class = EnemySerializer
    permission_classes = [IsAuthenticated]


class LevelViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Level.objects.\
        select_related("enemy_leader__ability", "enemy_leader__faction").\
        prefetch_related("enemies__faction", "enemies__color", "enemies__move", "enemies__passive_ability").\
        all()
    serializer_class = LevelSerializer

    @action(methods=['POST'], detail=True)
    def unlock_levels(self, request, pk=None):
        passed_level = Level.objects.filter(pk=pk).first()
        if not passed_level:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user = request.user
        user_open_levels = user.levels.all()
        levels_to_open = passed_level.related_levels.all()
        for level in levels_to_open:
            if level in user_open_levels:
                continue
            try:
                user.levels.add(level)
            except BaseException as er:
                print(er.message)
        serializer = RelatedLevelSerializer(levels_to_open, many=True)
        return Response(serializer.data)


class EnemyLeaderViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = EnemyLeader.objects.select_related("faction", "ability").all()
    serializer_class = EnemyLeaderSerializer
    permission_classes = [IsAuthenticated]
