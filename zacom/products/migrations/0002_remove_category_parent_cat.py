# Generated by Django 5.0.1 on 2024-01-21 08:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='parent_cat',
        ),
    ]
