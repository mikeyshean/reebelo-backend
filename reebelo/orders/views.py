import logging
from dataclasses import asdict

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from reebelo.core.exceptions import NotFoundError
from reebelo.shipments.api import ShipmentApi

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

    def retrieve(self, request, pk):
        order = OrderService.get_by_id(id=pk)
        if not order:
            return Response("Order not found", status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def delete(self, request, pk: str):
        try:
            OrderService.delete(id=pk)
            return Response(status=status.HTTP_200_OK)
        except NotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["get"], url_path="shipments")
    def get_order_shipment(self, request, pk):
        try:
            shipmentDto = ShipmentApi.get_by_order_id(orderId=pk)
            return Response(asdict(shipmentDto), status=status.HTTP_200_OK)
        except ValidationError as e:
            errors = {}
            for k, v in e.detail.items():
                errors[k] = map(lambda detail: detail.title(), v)
            return Response(errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except NotFoundError:
            return Response(status=status.HTTP_404_NOT_FOUND)
