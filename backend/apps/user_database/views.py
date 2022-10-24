from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.accounts.models import CustomUser
from apps.enemies.models import Enemy, EnemyLeader
from apps.user_database.permissions import IsOwner
from apps.user_database.serializers import DatabaseSerializer, UserResourceSerializer


class UserDatabaseViewSet(GenericViewSet):
    """user_database, id: user_id"""
    authentication_classes = [TokenAuthentication]

    def retrieve(self, request, pk=None):
        queryset = CustomUser.objects.filter(pk=pk).first()
        queryset_enemy = Enemy.objects.select_related("faction", "color", "move", "passive_ability").all()
        queryset_enemy_leader = EnemyLeader.objects.select_related("faction", "ability").all()
        serializer = DatabaseSerializer(dict(
            user_database=queryset,
            resources=queryset,
            enemies=queryset_enemy,
            enemy_leaders=queryset_enemy_leader,
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
