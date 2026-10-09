from django.db import models
from django.contrib.auth.models import User

class ProdutoQuerySet(models.QuerySet):
    """QuerySet customizado para reutilizar filtros encadeados."""
    def disponiveis(self):
        return self.filter(ativo=True, estoque__gt=0)


class ProdutoManager(models.Manager):
    """Manager customizado que adiciona o método .disponiveis() aos produtos."""
    def get_queryset(self):
        return ProdutoQuerySet(self.model, using=self._db)

    def disponiveis(self):
        return self.get_queryset().disponiveis()


class PerfilVendedor(models.Model):
    """
    Relacionamento OneToOne (1:1):
    Cada usuário do sistema pode ter no máximo UM perfil de vendedor, 
    e cada perfil pertence a APENAS UM usuário.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='perfil_vendedor'
    )
    nome_loja = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome_loja


class Tag(models.Model):
    """Categorias/Etiquetas para produtos."""
    nome = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nome


class Produto(models.Model):
    """
    Relacionamentos:
    - ForeignKey (1:N): Um Vendedor tem VÁRIOS Produtos, mas um Produto pertence a APENAS UM Vendedor.
    - ManyToMany (N:N): Um Produto pode ter VÁRIAS Tags, e uma Tag pode estar em VÁRIOS Produtos.
    """
    vendedor = models.ForeignKey(
        PerfilVendedor, 
        on_delete=models.CASCADE, 
        related_name='produtos'
    )
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True)
    preco = models.DecimalField(max_digits=10, decimal_places=2)
    estoque = models.PositiveIntegerField(default=0)
    ativo = models.BooleanField(default=True)
    
    tags = models.ManyToManyField(
        Tag, 
        related_name='produtos', 
        blank=True
    )

    # Conectando o Manager Customizado
    objects = ProdutoManager()

    def __str__(self):
        return self.nome


class Pedido(models.Model):
    """
    Cabeçalho do Pedido efetuado por um Comprador.
    Relaciona-se com Produto via modelo intermediário (Through Model).
    """
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('CONFIRMADO', 'Confirmado'),
        ('CANCELADO', 'Cancelado'),
    ]

    comprador = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='pedidos'
    )
    produtos = models.ManyToManyField(
        Produto, 
        through='ItemPedido', 
        related_name='pedidos'
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')

    def __str__(self):
        return f"Pedido #{self.id} - {self.comprador.username}"


class ItemPedido(models.Model):
    """
    Tabela Intermediária (Through Model) entre Pedido e Produto.
    Guarda informações adicionais da transação, como quantidade e preço no momento da compra.
    """
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE, 
        related_name='itens'
    )
    produto = models.ForeignKey(
        Produto, 
        on_delete=models.CASCADE, 
        related_name='itens_pedidos'
    )
    quantidade = models.PositiveIntegerField(default=1)
    preco_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantidade}x {self.produto.nome} (Pedido #{self.pedido.id})"