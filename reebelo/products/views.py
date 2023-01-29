from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from .serializers import (
    CreateProductSerializer,
    ProductSerializer,
    UpdateProductSerializer,
)
from .service import ProductService


class ProductViewSet(ViewSet):
    def create(self, request):
        try:
            serializer = CreateProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            product = ProductService.create(
                name=data["name"],
                quantity=data["quantity"],
                price=data["price"],
            )
            response_serializer = ProductSerializer(product)
            return Response(response_serializer.data)
        except ValidationError as e:
            errors = {}
            for k, v in e.detail.items():
                errors[k] = map(lambda detail: detail.title(), v)
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def list(self, request):
        products = ProductService.list()

        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        try:
            serializer = UpdateProductSerializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            product = ProductService.update(id=pk, **data)
            response_serializer = ProductSerializer(product)
            return Response(response_serializer.data)
        except ValidationError as e:
            errors = {}
            for k, v in e.detail.items():
                errors[k] = map(lambda detail: detail.title(), v)
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
