# Generated by Django 4.1 on 2023-02-07 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='adress_line_1',
            new_name='address_line_1',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='adress_line_2',
            new_name='address_line_2',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('Completed', 'Completado'), ('Cancelled', 'Cancelado'), ('New', 'Nuevo'), ('Accepted', 'Aceptado')], default='New', max_length=50),
        ),
    ]
