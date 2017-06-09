from rest_framework import permissions
from rest_framework.compat import is_authenticated

class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user#если создатель заметеки и пользователь равны, то вернуть объект

class IsNotAuthenticated(permissions.BasePermission):#Не прошел фудентификацию
    def has_permission(self, request, view):
        if request.method == 'POST':
            return not is_authenticated(request.user) or request.user.is_staff #если аудентифицирован или пользователь с особыми правами
        else:
            return request.uder.is_staff or False #если польователь с особыми правами