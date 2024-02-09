from django.contrib import admin
from .models import EnderecoUsuario, PerfilUsuario

# Register your models here.


@admin.register(EnderecoUsuario)
class EnderecoUsuarioAdmin(admin.ModelAdmin):
    list_display = 'id', 'cep', 'endereco', 'numero', 'cidade',
    list_display_links = 'id', 'cep', 'endereco',
    ordering = '-id',
    
@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = 'id', 'user', 'cpf', 'endereco',
    list_display_links = 'id', 'user', 'cpf',
    ordering = '-id',
    

