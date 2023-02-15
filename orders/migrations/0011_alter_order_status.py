# Generated by Django 4.1 on 2023-02-11 00:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0010_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completado'), ('New', 'Nuevo'), ('Cancelled', 'Cancelado'), ('Accepted', 'Aceptado')], default='New', max_length=50),
        ),
    ]
