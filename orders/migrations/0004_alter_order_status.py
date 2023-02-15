# Generated by Django 4.1 on 2023-02-08 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'Nuevo'), ('Completed', 'Completado'), ('Accepted', 'Aceptado'), ('Cancelled', 'Cancelado')], default='New', max_length=50),
        ),
    ]