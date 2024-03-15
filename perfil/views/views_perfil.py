from django.views import View
from django.http import HttpResponse 
from django.shortcuts import  render,get_object_or_404, redirect
from perfil.models import PerfilUsuario
from django.contrib.auth.models import User
from perfil.forms import UserForm, PerfilForm
import copy
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from utils.utils import qtd_total_carrinho


class BasePerfil(View):
    template_name = 'perfil/criar.html'
    
    def setup(self, *args, **kwargs) -> None:
        super().setup( *args, **kwargs)
        
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        
        self.perfil = None
        
        if self.request.user.is_authenticated: # se o usuario estiver logado
            self.perfil = PerfilUsuario.objects.filter(user=self.request.user).first()
            self.contexto = {
                'userform':UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user,
                    ),
                    
                
                'perfilform': PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil,
                    usuario=self.request.user,
                ),
            }
            
        else:
            self.contexto = {
                'userform':UserForm(data=self.request.POST or None),
                'perfilform': PerfilForm(data=self.request.POST or None),
            }
        
        self.userform:UserForm = self.contexto['userform']
        self.perfilform:PerfilForm = self.contexto['perfilform']
        
        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html'
        
        self.renderizar = render(
            self.request,
            self.template_name,
            self.contexto
        )
        
    def get(self, *args, **kwargs):
        return self.renderizar
    
    
class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        
        
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            messages.error(
                self.request,
                'Existe erro no seu formulario. Verifique e envie novamente'
            )
            return self.renderizar
        
        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password1')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')
        # usuario logado (update)
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User, username=self.request.user.username
            )
            
            usuario.username = username
            if password:
                usuario.set_password(password)
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()
            
            if not self.perfil:
                self.perfilform.cleaned_data['user'] = usuario
                perfil = PerfilUsuario(**self.perfilform.cleaned_data)
                perfil.save()
                
            else:
                perfil = self.perfilform.save(commit=False)
                perfil.user = usuario
                perfil.save()
                
                
        #não logado (criar)
        else:
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()
            
            perfil = self.perfilform.save(commit=False)
            perfil.user = usuario
            perfil.save() 
        
        if password:
            autentica = authenticate(
                request=self.request,
                username=username,
                password=password
            )
            
            if autentica:
                login(request=self.request,user=usuario)
            
            
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()
        
        messages.success(
            self.request,
            "Seu cadastro foi realizado com sucesso"
        )

        messages.success(
            self.request,
            "Login realizado com sucesso"
        )
        
        if qtd_total_carrinho(self.request.session['carrinho']) == 0:
            return redirect('perfil:atualizar')
        
        return redirect('produto:carrinho')     

class Login(View):    
    def setup(self, *args, **kwargs) -> None:
        super().setup(*args, **kwargs)
        
        self.renderizar = render(
            request= self.request,
            template_name = 'perfil/login.html'
        )
    def get(self, *args, **kwargs):
        return self.renderizar
    
    def post(self, *args, **kwargs):
        username = self.request.POST.get('username')
        password = self.request.POST.get('password')

        print(username, password)

        if not username or not password:
            messages.error(
                self.request,
                "Login invalido, username ou password não enviado."
            )

            return redirect('perfil:login')

        usuario = authenticate(self.request, username=username, password=password)

        if not usuario:
            messages.error(
                self.request,
                "Login invalido, esse usuário não existe."
            ) 
            return redirect('perfil:login')

        
        login(self.request, user=usuario)

        messages.success(
            self.request,
            "Usuario logado com sucesso"
        )

        return redirect('produto:carrinho')
    
class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        logout(self.request)

        self.request.session['carrinho'] = carrinho
        self.request.session.save()
        return redirect('produto:lista')
    