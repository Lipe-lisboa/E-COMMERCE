from django.contrib import admin
from .models import PerfilUsuario

# Register your models here.


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = 'id', 'user', 'cpf','endereco'
    list_display_links = 'id', 'user', 'cpf',
    ordering = '-id',
    

    

