from django.db import models
from django.contrib.auth.models import User
from utils.validate import valida_cpf, valida_cep
from django.core.exceptions import ValidationError
# Create your models here.


class PerfilUsuario(models.Model):
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5 )
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        default='SP',
        max_length= 2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    
    def __str__(self):
        if self.user.first_name:
            return self.user.first_name

        return self.user.username
    
    def clean(self, *args, **kwargs):
        #cleaned_data = self.cleaned_data
        #cpf = cleaned_data.get('cpf')
        #cep = cleaned_data.get('cep')
        
        error_messages = {}
        cpf = self.cpf
        cep = self.cep
        if not valida_cep(cep):
             error_messages['cep'] = 'cep invalido, tente novamente.'
        if not valida_cpf(cpf):

            error_messages['cpf'] = 'cpf invalido, tente novamente.'
            
        if error_messages:
            raise ValidationError(error_messages)
        
        super().clean(*args, **kwargs)
    
    

    
