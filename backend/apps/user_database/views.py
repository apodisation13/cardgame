from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.accounts.models import CustomUser
from apps.core.models import GameConst
from apps.enemies.models import Enemy, EnemyLeader, Season
from apps.user_database.permissions import IsOwner
from apps.user_database.serializers import DatabaseSerializer, UserResourceSerializer


class UserDatabaseViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    """user_database, id: user_id"""
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        parameters=[
            OpenApiParameter("id", OpenApiTypes.INT, OpenApiParameter.PATH),
        ],
        responses=DatabaseSerializer,
    )
    def retrieve(self, request, *args, **kwargs):
        user_database = CustomUser.objects.filter(pk=kwargs["pk"]).first()
        self.check_object_permissions(request, user_database)  # проверка разрешений!
        enemies = Enemy.objects.select_related("faction", "color", "move",
                                               "passive_ability").all()
        enemy_leaders = EnemyLeader.objects.select_related("faction", "ability").all()
        game_const = GameConst.objects.first()
        seasons = Season.objects.all()

        serializer = DatabaseSerializer(dict(
            user_database=user_database,
            resources=user_database,
            enemies=enemies,
            enemy_leaders=enemy_leaders,
            game_const=game_const,
            seasons=seasons,
        ),
            context=self.get_serializer_context()
        )
        return Response(serializer.data)

    def get_permissions(self):
        return [IsOwner()]

    def get_serializer_context(self):
        return {'request': self.request}


class UserResourceViewSet(GenericViewSet,
                          mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin,
                          ):

    authentication_classes = [TokenAuthentication]
    queryset = CustomUser.objects.all()
    serializer_class = UserResourceSerializer
    http_method_names = ["get", "patch"]

    def get_permissions(self):
        return [IsOwner()]
