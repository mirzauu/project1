# Generated by Django 5.0.1 on 2024-01-21 09:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_remove_category_parent_cat'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='slug',
            new_name='product_slug',
        ),
    ]