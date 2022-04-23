from rest_framework.permissions import BasePermission

from apps.cards.models import UserDeck, UserLeader, UserCard


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        # print(request.data)
        print(request.data.get('user'), request.user.id)
        return request.data.get('user') == request.user.id


class IsCardOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        print(obj)
        print(obj.id)
        usercard_obj = UserCard.objects.filter(id=obj.id).first()
        print(usercard_obj.user)
        return request.user == usercard_obj.user


class IsLeaderOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        print(obj)
        print(obj.id)
        userleader_obj = UserLeader.objects.filter(id=obj.id).first()
        print(userleader_obj.user)
        return request.user == userleader_obj.user


class IsDeckOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        print(obj)
        print(obj.id)
        userdeck_obj = UserDeck.objects.filter(deck_id=obj.id).first()
        print(userdeck_obj.user)
        return request.user == userdeck_obj.user
