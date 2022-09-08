from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

from apps.enemies.models import Enemy, EnemyLeader, Level, UserLevel, CustomUser
from apps.enemies.serializers import EnemyLeaderSerializer, EnemySerializer, LevelSerializer, IdNameLevelSerializer



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

    @action(methods=['POST'], detail=True, permission_classes=(IsAuthenticated, ))
    def unlock_levels(self, request, pk):
        """
        endpoint: api/v1/levels/pk/unlock_levels/
        Открываем уровни, связанные с пройденмым
        В body должен придоходить {'related_levels': [id1, id2, ..., idn]}
        """
        with transaction.atomic():
            request_user = request.user
            user_passed_level = UserLevel.objects.filter(
                user=request_user.id, level=pk).first()
            request_levels_id = request.data.get('related_levels')
            if not user_passed_level or not request_levels_id:
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data='no such opened levels or empty related_levels data'
                )

            user_passed_level.finished = True
            user_passed_level.save()
            user_open_levels = request_user.levels.all()
            new_opened_levels = Level.objects.filter(id__in=request_levels_id)
            new_user_levels = [level for level in new_opened_levels
                               if level not in user_open_levels]
            request_user.levels.add(*new_user_levels)

            serializer = IdNameLevelSerializer(new_user_levels, many=True)
        return Response(serializer.data)

    @action(methods=['DELETE'], detail=False)
    def delete_open_levels(self, request):
        """
        endpoint: api/v1/levels/delete_open_levels/
        Удаление всех открытых уровней пользователя кроме Уровня 1
        В body должен придоходить {'user': user_id}
        """
        request_data_user_id = request.data.get('user')
        if not request_data_user_id:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='empty request body')

        user = CustomUser.objects.filter(id=request_data_user_id).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND,
                            data='no such user in game')
        deleted_levels = UserLevel.objects.filter(user=user.id).exclude(level=1).delete()
        UserLevel.objects.filter(user=user.id, level=1).update(finished=False)
        return Response(f'{deleted_levels[0]} levels deleted')


class EnemyLeaderViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = EnemyLeader.objects.select_related("faction", "ability").all()
    serializer_class = EnemyLeaderSerializer
    permission_classes = [IsAuthenticated]
