# Generated by Django 3.1 on 2023-02-13 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_auto_20230213_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Cancelled', 'Cancelado'), ('Completed', 'Completado'), ('Accepted', 'Aceptado'), ('New', 'Nuevo')], default='New', max_length=50),
        ),
    ]