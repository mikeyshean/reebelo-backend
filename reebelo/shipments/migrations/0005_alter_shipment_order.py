# Generated by Django 4.1.4 on 2023-01-31 07:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_amount_per_unit'),
        ('shipments', '0004_remove_shipment_id_alter_shipment_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipment',
            name='order',
            field=models.OneToOneField(help_text='Order associated with shipment', on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='shipment', serialize=False, to='orders.order'),
        ),
    ]
