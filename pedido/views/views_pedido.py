from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse


class PagarPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse("pagar")
    
class SalvarPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse("fechar")
    
class DetalhePedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse("detalhe pedido")