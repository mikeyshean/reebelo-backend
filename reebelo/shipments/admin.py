from django.contrib import admin

from reebelo.shipments.models import Shipment


@admin.register(Shipment)
class ShipmentAdmin(admin.ModelAdmin):
    list_display = ("id", "recipient_name")
