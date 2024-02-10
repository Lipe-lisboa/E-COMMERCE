
from django.urls import path
from pedido.views import views_pedido

app_name = 'pedido'

urlpatterns = [
    path('', views_pedido.PagarPedido.as_view() ,name='pagar'),
    path('fecharpedido/',views_pedido.FecharPedido.as_view() ,name='fecharpedido'),
    path('detalhe/',views_pedido.DetalhePedido.as_view(),name='detalhe'),
]