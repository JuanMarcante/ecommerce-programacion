# Generated by Django 4.1 on 2023-02-09 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_variation_variation_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('talla', 'talla'), ('color', 'color')], max_length=100),
        ),
    ]
