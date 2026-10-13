from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ItemPedido

@receiver(post_save, sender=ItemPedido)
def atualizar_estoque_ao_comprar(sender, instance, created, **kwargs):
    if created:
        produto = instance.produto
        if produto.estoque >= instance.quantidade:
            produto.estoque -= instance.quantidade
            produto.save()
        else:
            raise ValueError(f"Estoque insuficiente para o produto '{produto.nome}'.")