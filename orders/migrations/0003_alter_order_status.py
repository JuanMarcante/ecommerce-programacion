# Generated by Django 4.1 on 2023-02-08 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_rename_adress_line_1_order_address_line_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelado'), ('Accepted', 'Aceptado'), ('Completed', 'Completado'), ('New', 'Nuevo')], default='New', max_length=50),
        ),
    ]
