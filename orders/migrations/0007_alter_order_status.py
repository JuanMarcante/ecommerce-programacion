# Generated by Django 4.1 on 2023-02-09 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('New', 'Nuevo'), ('Cancelled', 'Cancelado'), ('Completed', 'Completado'), ('Accepted', 'Aceptado')], default='New', max_length=50),
        ),
    ]
