from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Sum, F, Value, DecimalField
from django.db.models.functions import Coalesce

from .models import PerfilVendedor, Tag, Produto, Pedido
from .serializers import (
    PerfilVendedorSerializer, TagSerializer, 
    ProdutoSerializer, PedidoSerializer
)
from .permissions import IsOwnerOrReadOnly


class PerfilVendedorViewSet(viewsets.ModelViewSet):
    queryset = PerfilVendedor.objects.all()
    serializer_class = PerfilVendedorSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    @action(detail=False, methods=['get'], url_path='relatorio-faturamento')
    def relatorio_faturamento(self, request):
        vendedores = PerfilVendedor.objects.annotate(
            total_faturado=Coalesce(
                Sum(
                    F('produtos__itens_pedidos__quantidade') * F('produtos__itens_pedidos__preco_unitario'),
                    output_field=DecimalField()
                ),
                Value(0, output_field=DecimalField())
            )
        ).values('id', 'nome_loja', 'total_faturado')

        return Response(list(vendedores))


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ProdutoViewSet(viewsets.ModelViewSet):
    serializer_class = ProdutoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        if self.request.query_params.get('apenas_disponiveis') == 'true':
            return Produto.objects.disponiveis()
        
        vendedor_id = self.request.query_params.get('vendedor')
        if vendedor_id:
            return Produto.objects.filter(vendedor__id=vendedor_id)

        return Produto.objects.all()


class PedidoViewSet(viewsets.ModelViewSet):
    serializer_class = PedidoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Retorna apenas os pedidos do comprador autenticado (usando o related_name 'pedidos')
        return self.request.user.pedidos.all()

    def perform_create(self, serializer):
        # Define o comprador logado automaticamente ao salvar o pedido
        serializer.save(comprador=self.request.user)