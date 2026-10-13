from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Operações de leitura (GET, HEAD, OPTIONS) são liberadas
        if request.method in permissions.SAFE_METHODS:
            return True

        # Para PerfilVendedor ou Produto, verifica a propriedade
        if hasattr(obj, 'user'):
            return obj.user == request.user
        elif hasattr(obj, 'vendedor'):
            return obj.vendedor.user == request.user
            
        return False