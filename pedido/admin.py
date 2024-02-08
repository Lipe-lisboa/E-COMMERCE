from django.contrib import admin
from .models import Pedido, ItemPedido
# Register your models here.

class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1 

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    list_display = 'id', 'usuario','status',
    list_display_links = 'id', 'usuario',
    ordering = '-id',
    
    inlines = [
        ItemPedidoInline,
        ]