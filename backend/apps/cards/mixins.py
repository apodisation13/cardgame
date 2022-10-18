from apps.cards.permissions import (IsCardOwner, IsDeckOwner, IsLeaderOwner,
                                    IsOwner)
from rest_framework.permissions import IsAdminUser, IsAuthenticated


class CardBaseMixin:
    def get_permissions(self):
        """get - только админ, post,patch - только тот юзер, который там в теле запроса. Для Card и Leader"""
        if self.action == "list":
            return [IsAdminUser()]
        elif self.action == "create":
            return [IsOwner()]
        elif self.action == "partial_update":
            return [IsCardOwner()]
        return []


class LeaderBaseMixin:
    def get_permissions(self):
        """get - только админ, post - только тот юзер, который там в теле запроса, patch - только тот который был"""
        if self.action == "list":
            return [IsAdminUser()]
        elif self.action == "create":
            return [IsOwner()]
        elif self.action == "partial_update":
            return [IsLeaderOwner()]
        return []


class DeckBaseMixin:
    def get_permissions(self):
        """Для КОЛОД: create - зарегенный, patch,delete-IsObjectOwner"""
        if self.action == "list":
            return [IsAdminUser()]
        elif self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["destroy", "partial_update"]:
            return [IsDeckOwner()]
        return []
