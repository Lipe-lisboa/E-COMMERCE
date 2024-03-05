from typing import Any
from django import forms
from . import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.validate import valida_cpf, valida_cep

class PerfilForm(forms.ModelForm):
    class Meta:
         model = models.PerfilUsuario    
         fields = '__all__' #todos
         exclude = ('user',)
         

        

class UserForm(forms.ModelForm):
    
    password1= forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Senha',
        help_text='Senha precisa ter mais que 6 caracteres'
    )
    
    password2= forms.CharField(
        required=False,
        widget=forms.PasswordInput(),
        label='Confirmação senha',
        help_text='Senha precisa ter mais que 6 caracteres'
    )
    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.usuario = usuario
        
    class Meta:
         model = User
         fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )
         
    def clean(self, *args, **kwargs):
        cleaned_data = self.cleaned_data
        username= cleaned_data.get('username')
        email = cleaned_data.get('email')
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        
        username_db = User.objects.all().filter(username=username).first()
        email_db = User.objects.all().filter(email=email).first()
        
        #usuario ja existe (update)
        if self.usuario:
            
            if username_db:
                if username != username_db.username:
                    self.add_error(
                        'username',
                        ValidationError(
                            'Usuário já existe', code='invalid'
                        )
                    )
            
            
            if email_db:
                if email != email_db.email:
                    self.add_error(
                        'email',
                        ValidationError(
                            'Email já existe', code='invalid'
                        )
                    )   
            if password1:
                if password1 != password2:
                    msg_error = ValidationError('Senhas não conferem', code='invalid')
                    
                    self.add_error(
                        'password1', 
                        msg_error
                    )
                
                    self.add_error(
                        'password2', 
                        msg_error
                    )
                    
                if len(password1) < 6:
                    msg_error = ValidationError('Senha tem menos que 6 caracteres', code='invalid')
                    
                    self.add_error(
                        'password1', 
                        msg_error
                    )
                
                    self.add_error(
                        'password2', 
                        msg_error
                    )
              
            
        #usuario não existe (criação)  
        else:
            if User.objects.all().filter(username=username).exists():
                self.add_error(
                    'username',
                    ValidationError(
                        'Usuário já existe', code='invalid'
                    )
                )
            if User.objects.all().filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError(
                        'Esse email já existe', code='invalid'
                    )
                )
                
            if not password1:
                self.add_error(
                    'password1',
                    ValidationError(
                        'Senha é obrigatoria', code='invalid'
                    )
                )

            if not password2:
                self.add_error(
                    'password2',
                    ValidationError(
                        'Senha é obrigatoria', code='invalid'
                    )
                )
                
            if password1 != password2:
                msg_error = ValidationError('Senhas não conferem', code='invalid')
                
                self.add_error(
                    'password1', 
                    msg_error
                )
            
                self.add_error(
                    'password2', 
                    msg_error
                )
                
            if password1  and len(password1)  < 6:
                msg_error = ValidationError('Senha tem menos que 6 caracteres', code='invalid')
                
                self.add_error(
                    'password1', 
                    msg_error
                )
            
                self.add_error(
                    'password2', 
                    msg_error
                )
        return super().clean(*args, **kwargs)