from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from reebelo.core.exceptions import NotFoundError
from reebelo.products.exceptions import InsufficientQuantity

from .serializers import (
    CreateProductSerializer,
    ProductSerializer,
    UpdateProductSerializer,
)
from .service import ProductService

ERROR_CODE_INSUFFICIENT_QUANTITY = "insufficient_quantity"


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
        except InsufficientQuantity as e:
            error = {"error_code": e.error.code, "message": e.error.message}
            return Response(error, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk: int):
        try:
            ProductService.delete(pk)
            return Response(status=status.HTTP_200_OK)
        except NotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
