from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.views import View
from produto.models import Produto, Variacao
from perfil.models import PerfilUsuario
from django.shortcuts import redirect, get_object_or_404, reverse, render
from django.contrib import messages
from utils.utils import qtd_total_carrinho
from django.db.models import Q

class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'
    paginate_by =1
    ordering = '-id'
    

class Busca(ListaProdutos):
    
    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
        self._valor_busca = ''
        
    def get_queryset(self):
        qs = super().get_queryset()
        self._valor_busca = self.request.GET.get('termo', '').strip() or self.request.session['termo']
        
        if not self._valor_busca:
            return qs
        
        self.request.session['termo'] = self._valor_busca 
        
        qs = qs.filter(
        Q(name__icontains=self._valor_busca) |
        Q(descricao_curta__icontains=self._valor_busca) |
        Q(descricao_longa__icontains=self._valor_busca)     
        )
        
        
        self.request.session.save()
        return qs
class DetalheProduto(DetailView):
    model =  Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_field = 'slug'
    
class AdicionarAoCarrinho(View):
    def get(self,*args, **kwargs):
        
#        if self.request.session.get('carrinho'):
#            del self.request.session['carrinho']
#            self.request.session.save()

        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
                   
        variacao_id = self.request.GET.get('vid')
        
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe.'
            )
            return redirect('produto:lista')
        
        variacao = get_object_or_404(Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto
        
        produto_id  = produto.id
        produto_nome  = produto.name
        variacao_nome = variacao.nome or ''
        preco_unitario  = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem =  produto.imagem
        
        
        if imagem:
            imagem = imagem.name
        else:
            imagem = ''
    
        
        
        if variacao_estoque < 1 :
            messages.error(
                self.request,
                'Estoque insuficiente'
            )
            return redirect(http_referer)
            
        
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()
            
        carrinho = self.request.session['carrinho']
        
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1
            
            if variacao_estoque < quantidade_carrinho:
                messages.error(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x '
                    f'no produto "{produto_nome} {variacao_nome}". Adicionamos {variacao_estoque}x '
                    f'no seu estoque'
                )
                
                quantidade_carrinho = variacao_estoque
            
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * \
                quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional']  = preco_unitario_promocional * \
                quantidade_carrinho
        else:
            carrinho[variacao_id] =  {
                'produto_id ' : produto_id,
                'produto_nome' : produto_nome,
                'variacao_nome' : variacao_nome,
                'variacao_id'  : variacao_id,
                'preco_unitario' : preco_unitario,
                'preco_unitario_promocional' : preco_unitario_promocional,
                'preco_quantitativo': preco_unitario,
                'preco_quantitativo_promocional': preco_unitario_promocional, 
                'quantidade' :quantidade,
                'slug' : slug,
                'imagem' : imagem,
            }
            
        self.request.session.save()
         
        messages.success(
           self.request,
           f'{produto_nome} {variacao_nome} adicionada ao seu carrinho {carrinho[variacao_id]['quantidade']}x'
        )
        return redirect(http_referer)
    
class RemoverDoCarrinho(View):
    def get(self, *args, **kwargs):
        
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
                   
        variacao_id = self.request.GET.get('vid')
        
        if not variacao_id:
            return redirect(http_referer)
        
        carrinho = self.request.session.get('carrinho')
        if not carrinho :
            return redirect(http_referer)
        
        if variacao_id not in carrinho :
            return redirect(http_referer)
        
        
        produto_remove = self.request.session['carrinho'][variacao_id]
        messages.success(
            self.request,
            f'Produto:{produto_remove["produto_nome"]}, removido com sucesso'
        )
        
        del  self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)
    
class Carrinho(View):
    def get(self, *args, **kwargs):
        
        context = {
            'carrinho': self.request.session.get('carrinho', {})
        }
        return render(
            self.request,
            'produto/carrinho.html',
            context
        )
    
class ResumoDaCompra(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        
        self.usuario = self.request.user
        self.perfil = PerfilUsuario.objects.filter(user=self.request.user)
        self.carrinho =  self.request.session.get('carrinho', {})
        
        contexto = {
            'carrinho' : self.carrinho,
            'usuario': self.usuario ,
            'perfil':self.perfil.first()
        }
        self.renderizar = render(
            request=self.request,
            template_name='produto/resumodacompra.html',
            context=contexto
            
        )
        
    
    def get(self, *args, **kwargs):
        
        if not self.request.user.is_authenticated:
            return redirect('perfil:login')
        
        if not self.perfil.exists():
            messages.error(
                self.request,
                'Usuário sem perfil'
            )
            return redirect('perfil:criar')
            
        if not self.carrinho:
            messages.error(
                self.request,
                'Carrinho vazio'
            )
            return redirect('produto:lista')
        
        return self.renderizar
    