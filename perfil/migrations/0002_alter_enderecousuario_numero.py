# Generated by Django 5.0.2 on 2024-02-09 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enderecousuario',
            name='numero',
            field=models.CharField(max_length=5),
        ),
    ]
