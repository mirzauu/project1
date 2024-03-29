# Generated by Django 5.0.1 on 2024-02-24 09:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_alter_order_order_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='order_status',
            field=models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Delivered', 'Delivered'), ('Shipped', 'Shipped'), ('Cancelled_Admin', 'Cancelled Admin'), ('Cancelled_User', 'Cancelled User'), ('Returned', 'Returned'), ('Return Status', 'Returned Status')], default='New', max_length=20),
        ),
        migrations.AlterField(
            model_name='returnrequest',
            name='order_product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='return_requests', to='orders.orderproduct'),
        ),
    ]
