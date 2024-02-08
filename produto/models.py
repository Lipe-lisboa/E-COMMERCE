from django.db import models
from utils.validate import resize_image

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
    
    preço_marketing = models.FloatField(default=0)
    preço_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples'),
        )
    )
    
    def save(self, *args, **kwargs):
        super_save = super().save(*args, **kwargs)
        
        if self.imagem:
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
        if self.name:
            return self.name
        
        return self.prduto
    
    