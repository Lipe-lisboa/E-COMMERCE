from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views import View
from django.http import HttpResponse
from produto.models import Produto, Variacao
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

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
        variacao_id = self.request.GET.get('vid')
        
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não enviado'
            )
            return redirect('produto:lista')
        
        variacao = get_object_or_404(Variacao, id = variacao_id)
        
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
            
        carrinho = self.request.session.get('carrinho')
        
        if variacao_id in carrinho:
            ...
        else:
            ...
        return HttpResponse(f'{variacao.nome} {variacao.produto}')
    
class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse("remove car")
    
class Carrinho(View):
    def get(self, *args, **kwargs):
        return HttpResponse("car")
    
class Finalizar(View):
    def get(self, *args, **kwargs):
        return HttpResponse("finalizar")
    