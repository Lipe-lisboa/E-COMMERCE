from django.contrib import admin
from .models import Produto, Variacao

# Register your models here.

@admin.register(Variacao)
class VariacaoAdmin(admin.ModelAdmin):
    list_display = 'id','nome', 'produto', 'stoque',
    list_display_links = 'id','nome',
    ordering = '-id',

class VariacaoInline(admin.TabularInline):
    model = Variacao
    
    extra = 1
    
@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    list_display = 'id', 'name', 'tipo',
    list_display_links = 'name',
    search_fields = 'id', 'name', 'slug',
    list_per_page = 10
    ordering = '-id',
    prepopulated_fields = {
        'slug': ('name',)
    }
    
    inlines = VariacaoInline,
    
