# Generated by Django 5.0.1 on 2024-02-16 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_orderproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='grand_totol',
            field=models.DecimalField(decimal_places=2, max_digits=12, null=True),
        ),
    ]
