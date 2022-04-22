from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        print(request.data)
        print(request.data.get('user'), request.user.id)
        return request.data.get('user') == request.user.id
