from rest_framework import serializers

from reebelo.orders.models import Order


class ProductSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=8, decimal_places=2)


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "product",
            "quantity",
            "amount_per_unit",
            "amount_total",
        )


class CreateOrderSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    quantity = serializers.IntegerField()


class UpdateOrderShipmentSerializer(serializers.Serializer):
    recipient_name = serializers.CharField(max_length=128)
    tracking_company_id = serializers.CharField()
    tracking_number = serializers.CharField(max_length=128)
