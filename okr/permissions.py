# reune_app/okr/permissions.py

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permissão customizada para permitir que apenas os donos de um objeto
    possam editá-lo ou deletá-lo. Outros usuários podem apenas visualizar.
    """
    def has_object_permission(self, request, view, obj):
        # Permissões de leitura (GET, HEAD, OPTIONS) são permitidas para
        # qualquer requisição, desde que o usuário esteja autenticado.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Permissões de escrita (PUT, PATCH, DELETE) só são permitidas
        # se o 'responsavel' pelo objeto for o mesmo usuário que fez a requisição.
        return obj.responsavel == request.user