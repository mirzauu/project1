# Generated by Django 5.0.1 on 2024-02-28 15:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallettransaction',
            name='transaction_type',
            field=models.CharField(choices=[('CREDIT', 'CREDIT'), ('DEBIT', 'DEBIT')], max_length=10),
        ),
    ]
