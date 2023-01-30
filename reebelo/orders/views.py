import logging

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from reebelo.core.exceptions import NotFoundError

from .serializers import CreateOrderSerializer, OrderSerializer
from .service import OrderService

logger = logging.getLogger(__name__)


class OrderViewSet(ViewSet):
    def create(self, request):
        try:
            serializer = CreateOrderSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            data = serializer.validated_data
            result = OrderService.create(
                product_id=data["product_id"],
                quantity=data["quantity"],
            )

            if not result.success:
                error = {
                    "error_code": result.error.code,
                    "message": result.error.message,
                }
                return Response(error, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            response_serializer = OrderSerializer(result.data)
            return Response(response_serializer.data)
        except ValidationError as e:
            errors = {}
            for k, v in e.detail.items():
                errors[k] = map(lambda detail: detail.title(), v)
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def list(self, request):
        products = OrderService.list()

        serializer = OrderSerializer(products, many=True)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        return Response(status=status.HTTP_200_OK)

    def delete(self, request, pk: int):
        try:
            OrderService.delete(id=pk)
            return Response(status=status.HTTP_200_OK)
        except NotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
