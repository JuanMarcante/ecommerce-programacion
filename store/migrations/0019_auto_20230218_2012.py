# Generated by Django 3.1 on 2023-02-18 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0018_auto_20230214_1927'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
    ]