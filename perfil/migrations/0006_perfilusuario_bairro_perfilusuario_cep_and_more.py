# Generated by Django 5.0.2 on 2024-02-20 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0005_alter_enderecousuario_cep'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfilusuario',
            name='bairro',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='cep',
            field=models.CharField(max_length=8, null=True),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='cidade',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='complemento',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='estado',
            field=models.CharField(choices=[('AC', 'Acre'), ('AL', 'Alagoas'), ('AP', 'Amapá'), ('AM', 'Amazonas'), ('BA', 'Bahia'), ('CE', 'Ceará'), ('DF', 'Distrito Federal'), ('ES', 'Espírito Santo'), ('GO', 'Goiás'), ('MA', 'Maranhão'), ('MT', 'Mato Grosso'), ('MS', 'Mato Grosso do Sul'), ('MG', 'Minas Gerais'), ('PA', 'Pará'), ('PB', 'Paraíba'), ('PR', 'Paraná'), ('PE', 'Pernambuco'), ('PI', 'Piauí'), ('RJ', 'Rio de Janeiro'), ('RN', 'Rio Grande do Norte'), ('RS', 'Rio Grande do Sul'), ('RO', 'Rondônia'), ('RR', 'Roraima'), ('SC', 'Santa Catarina'), ('SP', 'São Paulo'), ('SE', 'Sergipe'), ('TO', 'Tocantins')], default='SP', max_length=2),
        ),
        migrations.AddField(
            model_name='perfilusuario',
            name='numero',
            field=models.CharField(max_length=5, null=True),
        ),
        migrations.AlterField(
            model_name='perfilusuario',
            name='endereco',
            field=models.CharField(max_length=50, null=True),
        ),
    ]