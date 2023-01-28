from rest_framework import serializers

from reebelo.products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "price", "quantity")


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "price", "quantity")


class UpdateProductSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=128)
    price = serializers.DecimalField(decimal_places=2, max_digits=8)
    decrease_quantity = serializers.IntegerField()
    increase_quantity = serializers.IntegerField()

    def validate(self, data):
        """
        Validation of decrease_quantity and end increase_quantity.
        """

        if data.get("decrease_quantity") and data.get("increase_quantity"):
            raise serializers.ValidationError(
                "Either increase or decrease quanitity, not both."
            )

        return data
