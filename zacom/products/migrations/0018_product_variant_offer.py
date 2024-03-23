# Generated by Django 5.0.1 on 2024-03-17 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_remove_product_variant_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='product_variant',
            name='offer',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
    ]