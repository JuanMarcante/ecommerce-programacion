# Generated by Django 4.1 on 2023-02-08 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completado'), ('Accepted', 'Aceptado'), ('New', 'Nuevo'), ('Cancelled', 'Cancelado')], default='New', max_length=50),
        ),
    ]
