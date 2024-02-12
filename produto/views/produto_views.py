from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views import View
from django.http import HttpResponse
from produto.models import Produto

class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by = 3
    
class DetalheProduto(DetailView):
    model =  Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_field = 'slug'
    
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
    