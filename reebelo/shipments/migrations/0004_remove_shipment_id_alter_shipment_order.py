# Generated by Django 4.1.4 on 2023-01-30 11:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_amount_per_unit'),
        ('shipments', '0003_alter_shipment_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shipment',
            name='id',
        ),
        migrations.AlterField(
            model_name='shipment',
            name='order',
            field=models.OneToOneField(help_text='Order associated with shipment', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='order', serialize=False, to='orders.order'),
        ),
    ]
