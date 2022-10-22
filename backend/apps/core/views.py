from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from apps.core.models import Faction, GameConst
from apps.core.serializers import FactionSerializer, GameConstSerializer


class FactionViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Faction.objects.all()
    serializer_class = FactionSerializer


class GameConstApiView(GenericViewSet, mixins.ListModelMixin):
    queryset = GameConst.objects.all()
    serializer_class = GameConstSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Для того, чтобы по запросу /api/v1/game_const/ брался только первый элемент"""
        return self.queryset.first()

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=False)
        return Response(serializer.data)
