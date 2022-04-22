from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from apps.accounts.models import CustomUser
from apps.user_database.serializers import UserDatabaseSerializer


class UserDatabaseViewSet(GenericViewSet, mixins.RetrieveModelMixin):
    """user_database, id: user_id"""
    queryset = CustomUser.objects. \
        prefetch_related("u_c__card__color",
                         "u_c__card__type",
                         "u_c__card__faction",
                         "u_c__card__ability",
                         "u_c__card__passive_ability",
                         "u_l__leader__faction",
                         "u_l__leader__ability",
                         "u_l__leader__passive_ability",
                         "u_level__level__enemies__faction",
                         "u_level__level__enemies__color",
                         "u_level__level__enemies__move",
                         "u_level__level__enemies__passive_ability",
                         "u_level__level__enemy_leader__faction",
                         "u_level__level__enemy_leader__ability",
                         "u_d__deck__cards__type",
                         "u_d__deck__cards__faction",
                         "u_d__deck__cards__ability",
                         "u_d__deck__cards__color",
                         "u_d__deck__cards__passive_ability",
                         "u_d__deck__leader__faction",
                         "u_d__deck__leader__ability",
                         "u_d__deck__leader__passive_ability",
                         ). \
        all()
    serializer_class = UserDatabaseSerializer
