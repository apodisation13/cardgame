from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.accounts.models import CustomUser
from apps.user_database.serializers import UserDatabaseSerializer


class UserDatabaseViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    """user_database, id: user_id"""
    queryset = CustomUser.objects.all()
    serializer_class = UserDatabaseSerializer
