from rest_framework import mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from apps.core.models import Faction, GameConst
from apps.core.serializers import FactionSerializer, GameConstSerializer


class FactionViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Faction.objects.all()
    serializer_class = FactionSerializer


class GameConstApiView(APIView):
    queryset = GameConst.objects.first()
    serializer_class = GameConstSerializer(queryset)
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(self.serializer_class.data)
