# Generated by Django 5.0.2 on 2024-02-08 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pedido', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pedido',
            options={'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
        migrations.RenameField(
            model_name='pedido',
            old_name='user',
            new_name='usuario',
        ),
    ]