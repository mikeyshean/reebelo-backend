from rest_framework import serializers

from reebelo.shipments.models import Shipment, TrackingCompany


class TrackingCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = TrackingCompany
        fields = ("id", "name")


class UpsertShipmentSerializer(serializers.Serializer):
    tracking_company_id = serializers.CharField()
    tracking_number = serializers.CharField(max_length=128, allow_null=True)


class ShipmentSerializer(serializers.ModelSerializer):
    tracking_company = TrackingCompanySerializer()

    class Meta:
        model = Shipment
        fields = ("order_id", "tracking_number", "tracking_company")
