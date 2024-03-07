
from django.urls import path
from pedido.views import views_pedido

app_name = 'pedido'

urlpatterns = [
    path('', views_pedido.PagarPedido.as_view() ,name='pagar'),
    path('salvarpedido/',views_pedido.SalvarPedido.as_view() ,name='salvarpedido'),
    path('lista', views_pedido.ListaPedido.as_view(), name='lista'),
    path('detalhe/',views_pedido.DetalhePedido.as_view(),name='detalhe'),
]