# Generated by Django 5.0.1 on 2024-01-30 18:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_rename_atribute_value_atribute_value_atribute_value_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_variant',
            name='variant_name',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
