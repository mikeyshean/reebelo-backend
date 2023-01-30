# Generated by Django 4.1.4 on 2023-01-30 11:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_amount_per_unit'),
        ('shipments', '0002_alter_trackingcompany_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='order',
            field=models.ForeignKey(help_text='Order associated with shipment', on_delete=django.db.models.deletion.CASCADE, related_name='order', to='orders.order', unique=True),
        ),
    ]