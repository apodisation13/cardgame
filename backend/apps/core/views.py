from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.core.models import Faction
from apps.core.serializers import FactionSerializer


class FactionViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Faction.objects.all()
    serializer_class = FactionSerializer
