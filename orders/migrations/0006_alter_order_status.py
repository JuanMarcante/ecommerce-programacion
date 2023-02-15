# Generated by Django 4.1 on 2023-02-09 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Accepted', 'Aceptado'), ('New', 'Nuevo'), ('Completed', 'Completado'), ('Cancelled', 'Cancelado')], default='New', max_length=50),
        ),
    ]