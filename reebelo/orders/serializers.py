from rest_framework import serializers

from reebelo.orders.models import Order


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)


class TrackingCompanySerializer(serializers.Serializer):
    name = serializers.CharField()


class ShipmentSerializer(serializers.Serializer):
    tracking_number = serializers.CharField()
    tracking_company = TrackingCompanySerializer()


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    shipment = ShipmentSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "product",
            "quantity",
            "amount_per_unit",
            "amount_total",
            "shipment",
        )


class CreateOrderSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField()


class UpdateOrderSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)
