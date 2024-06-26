# Generated by Django 5.0.1 on 2024-01-21 08:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Atribute',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atribute_name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand_name', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Atribute_value',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('atribute_value', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('atribute', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.atribute')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat_name', models.CharField(max_length=50, unique=True)),
                ('cat_slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('parent_cat', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=200, unique=True)),
                ('slug', models.SlugField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('is_available', models.BooleanField(default=True)),
                ('created_date', models.DateField(auto_now_add=True)),
                ('modified_date', models.DateTimeField(auto_now=True)),
                ('product_brand', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.brand')),
                ('product_catg', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product_Variant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_id', models.CharField(max_length=30)),
                ('max_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('stock', models.IntegerField()),
                ('product_variant_slug', models.SlugField(blank=True, max_length=200, unique=True)),
                ('thumbnail_image', models.ImageField(upload_to='photos/product_varient')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('atributes', models.ManyToManyField(related_name='attributes', to='products.atribute_value')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.AddConstraint(
            model_name='product_variant',
            constraint=models.UniqueConstraint(condition=models.Q(('sku_id__isnull', False)), fields=('product', 'sku_id'), name='Unique skuid must be provided'),
        ),
    ]
