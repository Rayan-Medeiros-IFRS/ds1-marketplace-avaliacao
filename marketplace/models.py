from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=200)
    """Produto — relaciona-se com Vendedor (ForeignKey) e Tag (ManyToMany)"""
class Pedido(models.Model):
    nome = models.CharField(max_length=200)
    """Pedido — relaciona-se com Produtos por meio de uma tabela intermediária (through model), guardando quantidade e preço no momento da compra"""
class PerfilVendedor(models.Model):
    nome = models.CharField(max_length=200)
    """PerfilVendedor — relação OneToOne com o usuário (User)"""
# Create your models here.