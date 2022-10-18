from apps.core.models import Faction  # , UserActionsJson
from apps.core.serializers import \
    FactionSerializer  # , UserActionsJsonSerializer
from rest_framework import mixins
# from rest_framework.authentication import TokenAuthentication
# from rest_framework.response import Response
# from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

# from apps.news.permissions import IsAdminOrReadOnly


class FactionViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = Faction.objects.all()
    serializer_class = FactionSerializer


# class UserActionsApiView(APIView):
#     data_json = UserActionsJson.objects.first()
#     serializer = UserActionsJsonSerializer(data_json)
#     permission_classes = [IsAdminOrReadOnly, ]
#     authentication_classes = [TokenAuthentication]
#
#     def get(self, request):
#         return Response(self.serializer.data)
