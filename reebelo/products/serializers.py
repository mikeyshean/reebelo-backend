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


class UpdateProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=128)
    price = serializers.DecimalField(decimal_places=2, max_digits=8)
    reduce_quantity = serializers.IntegerField()
    increase_quantity = serializers.IntegerField()

    class Meta:
        fields = ("name", "price", "reduce_quantity", "increase_quantity")
