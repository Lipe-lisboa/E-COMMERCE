from django.db import models
from utils.resize_image import resize_image
from utils.create_slug import slugify_new
from utils.format_preco import format_preco

# Create your models here.


class Produto (models.Model):
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        
        
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, default=None, blank=True,null=True)
    
    descricao_curta = models.TextField(max_length=200)
    descricao_longa = models.TextField(max_length=255)
    imagem = models.ImageField(upload_to='imagem_produto/%Y/%m/', blank=True)
    
    preco_marketing = models.FloatField(default=0)
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variável'),
            ('S', 'Simples'),
        )
    )
    
    def get_preco_formatado (self):
        return format_preco(self.preco_marketing)
    get_preco_formatado.short_description = 'Preco'    
        
    def get_preco_promocional_formatado (self):
        return format_preco(self.preco_marketing_promocional)
    get_preco_promocional_formatado.short_description = 'Preco promocional' 
        
        
    def save(self, *args, **kwargs):
        
        if not self.slug:
           self.slug =  slugify_new(self.name)
           
        img_atual = self.imagem.name
        
        super_save =  super().save(*args, **kwargs)
        
        img_changed = False
        new_img = None

        if self.imagem:
            new_img = self.imagem
            img_changed = bool(new_img != img_atual)
            
        if img_changed:
            resize_image(self.imagem)        
         
        return super_save
        
    
    def __str__(self):
        return self.name
    
class Variacao(models.Model):
    
    class Meta: 
        verbose_name = 'Variação'
        verbose_name_plural = 'variações'
    nome  = models.CharField(max_length=100, blank=True, null=True)
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE
    )
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    stoque = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        if self.nome:
            return self.nome
        
        return self.prduto
    
    