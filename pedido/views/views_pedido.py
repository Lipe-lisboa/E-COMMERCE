from typing import Any
from django.views.generic import DetailView
from django.views import View
from django.http import  HttpResponse

from django.shortcuts import redirect, get_object_or_404, render, reverse
from django.contrib import messages
from utils.utils import qtd_total_carrinho, preco_total
from produto.models import Variacao
from pedido.models import Pedido, ItemPedido


class DispatchLoginRequired():
    
    def dispatch(self, *args, **kwargs):
        
        if not self.request.user.is_authenticated:
            return redirect('perfil:login')
        return super().dispatch( *args, **kwargs)
    

class PagarPedido(DispatchLoginRequired,DetailView):
    template_name = 'pedido/pagar.html'
    model = Pedido
    pk_url_kwarg = 'id'
    context_object_name = 'pedido'
    
    def get_queryset(self, *args, **kwargs):
        queryset =  super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(
            usuario=self.request.user
        )
        
        return queryset
    
    
    
    
class SalvarPedido(View):
    
    def get(self, *args, **kwargs):
        self.carrinho = self.request.session.get('carrinho', {})
        
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Usuário não logado.'
        )
            return redirect('perfil:login')
        
        if qtd_total_carrinho(self.carrinho) == 0:
            messages.error(
                self.request,
                'Carrinho vazio'
            )
            return redirect('produto:lista')
        
        carrinho_variacaoes_ids = [v for v in self.carrinho]
        bd_variacoes = list(
            Variacao.objects.filter(id__in=carrinho_variacaoes_ids)
        )
        
        for variacao in bd_variacoes:
            variacao_estoque = variacao.estoque
            vid = str(variacao.id)
            
            
            qtd_carrinho = self.carrinho[vid]['quantidade']
            preco_unt = self.carrinho[vid]['preco_unitario']
            preco_unt_promo = self.carrinho[vid]['preco_unitario_promocional']
            
            if qtd_carrinho > variacao_estoque:
                self.carrinho[vid]['quantidade'] = variacao_estoque
                self.carrinho[vid]['preco_quantitativo'] = variacao_estoque * preco_unt
                self.carrinho[vid]['preco_quantitativo_promocional'] = variacao_estoque * preco_unt_promo
                
                qtd_carrinho = variacao_estoque
                messages.error(
                    self.request,
                    'Estoque insuficiente para alguns produtos do seu carrinho. '
                    'Reduzimos a quantidade desses produtos. Por favor, verifique '
                    'quais produtos foram afetados abaixo:'
                )
                
                self.request.session.save()
                return redirect('produto:carrinho')

    
        qtd_tt_carrinho = qtd_total_carrinho(self.carrinho)
        vl_tt_carrinho = preco_total(self.carrinho)
        
        pedido = Pedido(
            usuario=self.request.user,
            total=vl_tt_carrinho,
            qtd_total=qtd_tt_carrinho,
            status='C'
            )
        
        pedido.save()
        
        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto = v['produto_nome'],
                    variacao= v['variacao_nome'],
                    variacao_id= v['variacao_id'],
                    preco=v['preco_unitario'],
                    preco_promocional=v['preco_unitario_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                    produto_id= v['produto_id '],
                    
                    
                    
                ) for v in self.carrinho.values()   
            ]
        )
        
        del self.request.session['carrinho']
        return redirect(
            reverse(
                'pedido:pagar',
                kwargs={
                    'id':pedido.id    
                }
                
            )
        )

class ListaPedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse("lista")
ListaPedido    
class DetalhePedido(View):
    def get(self, *args, **kwargs):
        return HttpResponse("detalhe pedido")