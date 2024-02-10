from django.views.generic.list import ListView
from django.views import View
from django.http import HttpResponse

class ListaProdutos(View):
    def get(self, *args, **kwargs):
        return HttpResponse("lista")
    
class DetalheProduto(View):
    def get(self,*args, **kwargs):
        return HttpResponse("detalhe produto")
    
class AdicionarAoCarrinho(View):
    def get(self,*args, **kwargs):
        return HttpResponse("add car")
    
class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse("remove car")
    
class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse("car")
    
class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse("finalizar")
    