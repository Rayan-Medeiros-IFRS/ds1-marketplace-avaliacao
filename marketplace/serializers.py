from rest_framework import serializers
from .models import PerfilVendedor, Tag, Produto, Pedido, ItemPedido


class PerfilVendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilVendedor
        fields = ['id', 'user', 'nome_loja', 'bio']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'nome']


class ProdutoSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Produto
        fields = ['id', 'vendedor', 'nome', 'descricao', 'preco', 'estoque', 'ativo', 'tags']


class ItemPedidoSerializer(serializers.ModelSerializer):
    produto_nome = serializers.ReadOnlyField(source='produto.nome')

    class Meta:
        model = ItemPedido
        fields = ['id', 'produto', 'produto_nome', 'quantidade', 'preco_unitario']


class PedidoSerializer(serializers.ModelSerializer):
    itens = ItemPedidoSerializer(many=True)

    class Meta:
        model = Pedido
        fields = ['id', 'comprador', 'status', 'criado_em', 'itens']

    def create(self, validated_data):
        itens_data = validated_data.pop('itens')
        pedido = Pedido.objects.create(**validated_data)
        
        for item_data in itens_data:
            ItemPedido.objects.create(pedido=pedido, **item_data)
            
        return pedido