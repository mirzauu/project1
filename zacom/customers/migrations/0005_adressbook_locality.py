# Generated by Django 5.0.1 on 2024-02-05 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_adressbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='adressbook',
            name='locality',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
