from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PerfilVendedorViewSet, 
    TagViewSet, 
    ProdutoViewSet, 
    PedidoViewSet
)

# Roteador automático do DRF para os ViewSets
router = DefaultRouter()
router.register(r'vendedores', PerfilVendedorViewSet, basename='vendedor')
router.register(r'tags', TagViewSet, basename='tag')
router.register(r'produtos', ProdutoViewSet, basename='produto')
router.register(r'pedidos', PedidoViewSet, basename='pedido')

urlpatterns = [
    path('', include(router.urls)),
]